# 环境准备

本工具依赖 playwright 工具伪装浏览器，获取 WWDC 字幕文件的下载链接，需要安装 playwright 工具，虽然依赖写在了 `requirements.txt` 中，但初次安装仍然需要手动执行

```shell
$ playwright install
```

后，才能执行工具。

# 使用说明

```shell
$ python wwdcSubTitleDownloader.py <wwdc video url>
```

执行完成后，文件夹内的 `full.srt` 为最终的字幕文件
