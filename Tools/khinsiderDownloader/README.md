# 说明

khinsider 下载器，仅提供获取专辑所有 flac 链接爬取，不提供下载。

# 用法

```shell
$ python3 downloader.py 'https:/url/to/album'
# for example
# python3 downloader.py 'https://downloads.khinsider.com/game-soundtracks/album/genshin-impact-outside-it-is-growing-dark-2025'
```

爬取成功的链接会保存到 `flac_links.txt` 中，失败的会保存在 `failed_logs.txt` 中
