import concurrent.futures
import os
import queue
import subprocess
import threading
import time
import yt_dlp

# ==================== 配置区 ====================
VIDEO_LIST_FILE = "video_list.txt"  # B站链接列表
OUTPUT_DIR = "text_result"  # 文本结果输出目录
TEMP_DOWNLOAD_DIR = "downloads"  # 临时下载目录
ERROR_LOG_FILE = "error_log.txt"  # 错误日志文件
START_SH_PATH = "./start.sh"  # 转换脚本路径

MAX_DOWNLOAD_WORKERS = 3  # 最大同时下载线程数 (网络并发)
MAX_TRANSCRIPTION_WORKERS = (
    1  # 最大同时转写任务数 (建议设为1，因为whisper极耗CPU/GPU)
)
# ================================================

# 全局锁，防止多线程同时写 error_log 造成冲突
log_lock = threading.Lock()
# 转写任务队列
transcribe_queue = queue.Queue()


def log_error(url: str, reason: str):
    """增量写入错误日志 (线程安全)"""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] 链接: {url} | 原因: {reason}\n"

    with log_lock:
        with open(ERROR_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_line)
    print(f"❌ 记录错误: {url} -> {reason}")


def download_video(url: str) -> str:
    """下载视频并输出为本地音频/视频文件，失败则抛出异常"""
    if not os.path.exists(TEMP_DOWNLOAD_DIR):
        os.makedirs(TEMP_DOWNLOAD_DIR, exist_ok=True)

    # 配置 yt-dlp
    ydl_opts = {
        # 仅下载音频或合并为 mp4 (whisper只需要音频，这里下普通视频格式即可)
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "outtmpl": os.path.join(TEMP_DOWNLOAD_DIR, "%(id)s.%(ext)s"),
        "http_headers": {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            "Referer": "https://www.bilibili.com/",
        },
        "quiet": True,
        "no_warnings": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # 获取信息并提取真实保存文件名
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)

        # 处理可能因格式合并导致的扩展名变更
        if not os.path.exists(filename):
            base, _ = os.path.splitext(filename)
            if os.path.exists(base + ".mp4"):
                filename = base + ".mp4"
            elif os.path.exists(base + ".mkv"):
                filename = base + ".mkv"

        return filename


def download_worker(url: str):
    """下载线程的任务处理"""
    url = url.strip()
    if not url or url.startswith("#"):
        return

    print(f"📥 开始下载/解析: {url}")
    try:
        file_path = download_video(url)
        print(f"✅ 下载成功: {url} -> {file_path}")
        # 下载成功后，推入转写队列
        transcribe_queue.put((url, file_path))
    except Exception as e:
        log_error(url, f"下载/解析失败: {str(e)}")


def transcribe_worker():
    """后台转写线程：不断从队列获取下载好的文件并调用 start.sh"""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR, exist_ok=True)

    while True:
        task = transcribe_queue.get()
        if task is None:  # 退出信号
            transcribe_queue.task_done()
            break

        url, video_path = task
        video_filename = os.path.basename(video_path)
        base_name = os.path.splitext(video_filename)[0]
        output_txt_path = os.path.join(OUTPUT_DIR, f"{base_name}.txt")

        print(f"🧠 开始语音转写: {video_filename} ...")

        try:
            # 异步/同步调用 start.sh 脚本
            cmd = [START_SH_PATH, video_path, output_txt_path]
            result = subprocess.run(
                cmd, capture_output=True, text=True, check=True
            )

            print(f"🎉 转写完成: {output_txt_path}")

        except subprocess.CalledProcessError as e:
            err_msg = e.stderr.strip() if e.stderr else str(e)
            log_error(url, f"Whisper转写脚本执行失败: {err_msg}")
        except Exception as e:
            log_error(url, f"转写过程未知错误: {str(e)}")
        finally:
            # 转写完成后清理本地临时视频文件，节省空间
            if os.path.exists(video_path):
                try:
                    os.remove(video_path)
                except Exception:
                    pass
            transcribe_queue.task_done()


def main():
    if not os.path.exists(VIDEO_LIST_FILE):
        print(f"❌ 未找到链接文件: {VIDEO_LIST_FILE}，请先创建！")
        return

    # 检查 start.sh 可执行权限
    if not os.access(START_SH_PATH, os.X_OK):
        print(
            f"⚠️ 正在为 {START_SH_PATH} 添加可执行权限 (chmod +x)..."
        )
        os.chmod(START_SH_PATH, 0o755)

    # 读取所有的 B 站链接
    with open(VIDEO_LIST_FILE, "r", encoding="utf-8") as f:
        urls = [
            line.strip()
            for line in f
            if line.strip() and not line.startswith("#")
        ]

    if not urls:
        print("⚠️ video_list.txt 中没有找到有效的链接！")
        return

    print(f"🚀 任务开始，共读取到 {len(urls)} 条链接。")

    # 1. 启动后台转写线程
    transcribe_threads = []
    for _ in range(MAX_TRANSCRIPTION_WORKERS):
        t = threading.Thread(target=transcribe_worker, daemon=True)
        t.start()
        transcribe_threads.append(t)

    # 2. 启动多线程下载池
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=MAX_DOWNLOAD_WORKERS
    ) as executor:
        executor.map(download_worker, urls)

    # 3. 等待所有转写任务完成
    transcribe_queue.join()

    # 4. 停止后台转写线程
    for _ in range(MAX_TRANSCRIPTION_WORKERS):
        transcribe_queue.put(None)
    for t in transcribe_threads:
        t.join()

    print("\n🏁 所有任务执行完毕！")
    print(f"📄 文本结果保存在: ./{OUTPUT_DIR}/")
    print(f"⚠️ 错误日志保存在: ./{ERROR_LOG_FILE}")


if __name__ == "__main__":
    main()
