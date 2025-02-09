![ffcuesplitter](https://img.shields.io/badge/ffcuesplitter-v1.0.25-blue)
![pyside6](https://img.shields.io/badge/pyside6-v6.8.1.1-blue)

# CUE 文件切分

目前仅支持任意格式音频分割为 flac 格式，不支持格式转换，不支持切换输出格式。如果想更自由地进行切分，请使用 [FFcuesplitter](https://github.com/jeanslack/FFcuesplitter)。

## 运行方式
系统中存在 ffmpeg，并且确保终端可以找到 ffmpeg。

1. run `pip3 install -r requirements.txt`
2. run `python3 main.py`

## 使用方式

运行后可以看到窗口:

<div style="text-align:center">
    <img src="imgs/main_page.png" alt="示例图片" width="600" />
</div>
如窗口内提示所述，你可以拖动 CUE 文件到窗口，或者点击按钮选择一个 CUE 文件。

如果是一个可以识别的 CUE 文件，则会列出该 CUE 下包含的歌曲，你可以滑动滚轮来查看歌曲信息

<div style="text-align:center">
    <img src="imgs/info_page.png" alt="示例图片" width="600" />
</div>

如果想要更换一个 CUE 文件，则拖动那个 CUE 文件到窗口内即可。

初始状态是没有设置保存（导出）路径的，需要点击按钮来选择一个文件夹，成功选择后如下图所示：

<div style="text-align:center">
    <img src="imgs/select_output_page.png" alt="示例图片" width="600" />
</div>

之后就可以点击按钮进行切分了。注意切分过程中需要等待一段时间，此时界面无法进行交互：

<div style="text-align:center">
    <img src="imgs/process_page.png" alt="示例图片" width="600" />
</div>

等待窗口提示 "文件切分完成" 完成即可：

<div style="text-align:center">
    <img src="imgs/success_hint_page.png" alt="示例图片" width="600" />
</div>
切分成功后会自动弹出目录页面。

# Thanks

1. FFcuesplitter: https://github.com/jeanslack/FFcuesplitter
2. PyQt 6
