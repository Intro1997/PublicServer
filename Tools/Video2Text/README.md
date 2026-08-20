# B23 视频链接转文本

## 核心文件目录结构
.
├── start.sh          # 视频转文字 Shell 脚本
├── batch_process.py  # 下方主 Python 脚本
├── video_list.txt    # 存放 B 站链接的文件 (一行一个)
├── downloads/        # (自动生成) 临时存放视频/音频
├── text_result/      # (自动生成) 存放转写出来的 txt 文件
└── error_log.txt     # (自动生成) 记录错误日志

## 使用方法

1. 将想要下载的链接存放进 video_list.txt 文件, 支持注释
```
https://www.bilibili.com/video/BV1xx411c7mD
https://www.bilibili.com/video/BV1GJ411x7h7
# 这是一条注释
https://www.bilibili.com/video/BV1234567890
```
2. 给 start.sh 赋予可执行权限 `chmod +x start.sh`

3. 运行解析脚本 `python batch_process.py`

## 环境配置 (以 mac 为例)

1. 安装 whisper-cpp 

`brew install whisper-cpp`

2. 创建存放模型的文件夹

```shell
# 1. 创建专门存放 whisper.cpp 模型的文件夹
mkdir -p ~/.cache/whisper.cpp

# 2. 从 Hugging Face 极速下载大型模型
curl -L -o ~/.cache/whisper.cpp/ggml-large-v3.bin \
  "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3.bin?download=true"

# 3. 下载 ggml-silero-v6.2.0.bin 并保存到缓存目录
curl -L -o ~/.cache/whisper.cpp/ggml-silero-v6.2.0.bin \
  https://huggingface.co/ggml-org/whisper-vad/resolve/main/ggml-silero-v6.2.0.bin
```
3. 安装 yt-dlp
```shell
pip install yt-dlp
```
