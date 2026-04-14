import asyncio
from pathlib import Path
from playwright.async_api import async_playwright, Route
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
import re
import sys

# 禁用 requests 的不安全请求警告（因为我们可能需要跳过 SSL 验证）
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def download_file_as_string(url):
    print("正在获取 ", url, " 对应的文件")
    try:
        # 同样在 requests 中加入 verify=False 以防万一
        response = requests.get(url, timeout=30, verify=False)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"下载失败: {e}")
        return None

TARGET_M3U8 = "cmaf.m3u8"

async def intercept_and_get_m3u8_url(wwdc_video_url):
    """不再拦截请求，直接从页面变量中抓取 URL。"""
    async with async_playwright() as p:
        # 使用 headless=True 即可，这种方法对 SSL 报错不敏感
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(ignore_https_errors=True)
        page = await context.new_page()

        print(f"🌐 正在解析页面数据: {wwdc_video_url}")

        try:
            # 访问页面
            await page.goto(wwdc_video_url, wait_until="domcontentloaded")
            
            # 方案 A：从页面静态脚本中直接找 URL
            # Apple 页面通常包含一个包含视频信息的 JSON
            content = await page.content()
            # 匹配类似 https://.../cmaf.m3u8 的字符串
            m3u8_matches = re.findall(r'https://[^\s"\'<>]*cmaf\.m3u8[^\s"\'<>]*', content)
            
            if m3u8_matches:
                # 拿第一个匹配到的
                m3u8_url = m3u8_matches[0]
                print(f"✅ 成功从页面源代码中提取到 M3U8 URL！")
                return m3u8_url

            # 方案 B：如果静态匹配不到，尝试执行 JS 获取
            m3u8_url = await page.evaluate("""() => {
                // 尝试从 Apple 的全局播放器对象中找
                try {
                    return document.querySelector('script[type="application/json"]#video_data').textContent;
                } catch(e) {
                    // 备选：查找页面所有字符串
                    return document.documentElement.innerHTML.match(/https:\/\/[^\\s"\'<>]*cmaf\.m3u8[^\\s"\'<>]*/)[0];
                }
            }""")

        except Exception as e:
            print(f"⚠️ 静态解析失败，这可能是因为页面结构改变。")
            m3u8_url = None
        finally:
            await browser.close()

        return m3u8_url
# --- 以下逻辑保持原样，仅确保 get_file_name 等辅助函数正常运作 ---

async def get_base_url(wwdc_video_url):
    final_m3u8_url = await intercept_and_get_m3u8_url(wwdc_video_url)
    if final_m3u8_url:
        # 移除 URL 中的 query 参数后再分割
        clean_url = final_m3u8_url.split("?")[0]
        return clean_url.rsplit("/", 1)[0]
    return None

def get_all_webvtt_content_from(index_file_content):
    return re.findall(r"sequence.*\.webvtt", index_file_content)

def download_subtitle(subtitle_url, save_file):
    try:
        response = requests.get(subtitle_url, verify=False, timeout=10)
        if response.status_code == 200:
            with open(save_file, "wb") as file:
                file.write(response.content)
            print(f"Downloaded {save_file}")
            return True
    except:
        pass
    print(f"Failed to download {save_file}")
    return False

async def download_webvtts(base_url, webvtt_items):
    print(f"尝试下载 {len(webvtt_items)} 个 webvtt 文件...")
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(download_subtitle, base_url + item, item)
                   for item in webvtt_items]
        for future in as_completed(futures):
            future.result()

async def get_webvtt_file_from(wwdc_video_url, output_file_name):
    base_url = await get_base_url(wwdc_video_url)
    if base_url:
        # 注意：部分年份的路径结构可能略有不同，这里沿用你的逻辑
        subtitle_base_url = base_url + "/subtitles/eng/"
        index_url = subtitle_base_url + "prog_index.m3u8"
        
        file_content = download_file_as_string(index_url)
        if file_content:
            all_webvtt_items = get_all_webvtt_content_from(file_content)
            if all_webvtt_items:
                await download_webvtts(subtitle_base_url, all_webvtt_items)
                merge_and_clean_subtitles(all_webvtt_items, output_file_name)
            else:
                print("❌ prog_index 文件中未找到 webvtt 序列。")
    else:
        print("❌ 无法获取 base_url。")

def merge_and_clean_subtitles(all_webvtt_file_path, output_file_name):
    print(f"正在合并到 {output_file_name}...")
    current_cnt = 1
    with open(output_file_name, "w", encoding='utf-8') as full_file:
        for webvtt in all_webvtt_file_path:
            if not Path(webvtt).exists():
                continue
            with open(webvtt, "r", encoding='utf-8') as file:
                content = file.read()
                # 简单的转换逻辑：去掉 WEBVTT 头，转换换行
                cleaned_content = re.sub(r'^WEBVTT\n', '', content)
                cleaned_content = re.sub(r'\n\s*\n', '\n', cleaned_content)
                if len(cleaned_content.strip()) > 0:
                    full_file.write(f"{current_cnt}\n" + cleaned_content.strip() + "\n\n")
                    current_cnt += 1
            print(f"Merged {webvtt}")
    
    is_remove = input("合并完成，是否删除缓存？[Y/N]: ")
    if is_remove.lower() == 'y':
        for f in Path(".").glob("sequence*.webvtt"):
            f.unlink()

def get_file_name(wwdc_url):
    pattern = r'wwdc(\d{4})/(\d+)'
    match = re.search(pattern, wwdc_url)
    if match:
        return f"wwdc{match.group(1)}-{match.group(2)}.srt"
    return "subtitle.srt"

def may_valid_wwdc_url(wwdc_url):
    return "developer.apple.com/videos/play/" in wwdc_url

if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = sys.argv[1]
        if may_valid_wwdc_url(url):
            asyncio.run(get_webvtt_file_from(url, get_file_name(url)))
            sys.exit(0)
    print("❌ URL 格式不正确")