#!/bin/zsh

set -e

# ==================== 配置区 ====================
MODEL_PATH="${HOME}/.cache/whisper.cpp/ggml-large-v3.bin"
LANGUAGE="zh"
# ================================================

show_help() {
  cat << EOF
用法: $(basename "$0") <输入视频路径> <输出文本路径> [选项]

描述:
  使用本地 whisper.cpp (large-v3 模型) 提取视频文件中的语音并转换为文本。
  内置“防死循环/防幻觉”算法，优化中文及带背景音视频的转写准确度。

参数:
  <输入视频路径>    需要提取文字的视频/音频文件路径
  <输出文本路径>    生成的纯文本 (.txt) 保存路径

选项:
  -h, --help        显示此帮助信息并退出
  -m, --model PATH  指定 custom GGML 模型路径 (默认: $MODEL_PATH)
  -l, --lang LANG   指定识别语言 (默认: $LANGUAGE)

示例:
  $(basename "$0") input.mp4 output.txt
EOF
}

# 1. 帮助选项校验
for arg in "$@"; do
  if [[ "$arg" == "-h" || "$arg" == "--help" ]]; then
    show_help
    exit 0
  fi
done

# 2. 位置参数校验
if [ "$#" -lt 2 ]; then
  echo "❌ 错误: 参数不足！" >&2
  show_help
  exit 1
fi

INPUT_VIDEO="$1"
OUTPUT_TXT="$2"
shift 2

while [[ "$#" -gt 0 ]]; do
  case $1 in
    -m|--model) MODEL_PATH="$2"; shift 2 ;;
    -l|--lang)  LANGUAGE="$2"; shift 2 ;;
    *) echo "❌ 未知参数: $1" >&2; show_help; exit 1 ;;
  esac
done

# 3. 依赖及文件校验
if ! command -v ffmpeg &> /dev/null; then
  echo "❌ 错误: 未找到 'ffmpeg' 命令" >&2
  exit 1
fi

if ! command -v whisper-cli &> /dev/null; then
  echo "❌ 错误: 未找到 'whisper-cli' 命令" >&2
  exit 1
fi

if [ ! -f "$INPUT_VIDEO" ]; then
  echo "❌ 错误: 输入视频文件不存在: '$INPUT_VIDEO'" >&2
  exit 1
fi

if [ ! -f "$MODEL_PATH" ]; then
  echo "❌ 错误: 未找到模型文件: '$MODEL_PATH'" >&2
  exit 1
fi

TEMP_AUDIO="$(mktemp /tmp/whisper_audio_XXXXXX.wav)"
trap 'rm -f "$TEMP_AUDIO"' EXIT

echo "🎬 正在提取并标准化音频 (16kHz 单声道)..."
ffmpeg -y -i "$INPUT_VIDEO" -ar 16000 -ac 1 -c:a pcm_s16le "$TEMP_AUDIO" -loglevel error

echo "🧠 正在调用 whisper.cpp 进行防幻觉转写..."
OUTPUT_BASE="${OUTPUT_TXT%.txt}"

# 核心优化：加入了 --no-repeat-ngram-size 和 --suppress-non-speech-tokens 参数
VAD_MODEL_PATH="$HOME/.cache/whisper.cpp/ggml-silero-v6.2.0.bin"

whisper-cli -m "$MODEL_PATH" \
            -f "$TEMP_AUDIO" \
            -l "$LANGUAGE" \
            -sns \
            --prompt "以下是中文普通话的转写稿，请不要重复标点和句子。" \
            --vad \
            --vad-model "$VAD_MODEL_PATH" \
            --no-speech-thold 0.6 \
            --entropy-thold 2.4 \
            --max-context 1 \
            --beam-size 1 \
            -otxt \
            -of "$OUTPUT_BASE" > /dev/null

echo "✅ 转换完成！文本已覆盖存入: $OUTPUT_TXT"
