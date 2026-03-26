import requests
from bs4 import BeautifulSoup
import sys
import time


def fetch_flac_links(initial_url, headers=None):
    """
    从初始页面提取MP3下载链接，然后访问每个链接提取FLAC下载链接。

    Args:
        initial_url (str): 初始页面URL（如专辑页面）。
        headers (dict): 请求头，默认包含常见User-Agent。

    Returns:
        list: FLAC链接列表。
    """

    if headers is None:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    # 1. 获取初始页面
    try:
        resp = requests.get(initial_url, headers=headers, timeout=10)
        resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"获取初始页面失败: {e}", file=sys.stderr)
        return []

    soup = BeautifulSoup(resp.text, "html.parser")

    # 2. 提取所有MP3下载链接
    mp3_links = []
    # 根据示例，MP3下载链接位于 td class="playlistDownloadSong" 中的 a 标签
    for td in soup.find_all("td", class_="playlistDownloadSong"):
        a_tag = td.find("a")
        if a_tag and a_tag.get("href"):
            mp3_links.append(a_tag["href"])

    print(f"找到 {len(mp3_links)} 个MP3下载链接")

    flac_links = []
    failed_logs = []

    # 3. 遍历每个MP3下载页面，提取FLAC链接
    for idx, mp3_url in enumerate(mp3_links, 1):
        print(f"处理第 {idx}/{len(mp3_links)} 个: {mp3_url}")
        mp3_url = "/" + mp3_url.split("/")[-1]
        try:
            resp = requests.get(initial_url + mp3_url, headers=headers, timeout=10)
            resp.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"  获取页面失败: {e}", file=sys.stderr)
            failed_logs.append(f"访问页面失败 {initial_url + mp3_url}  错误信息：{e}")
            continue

        page_soup = BeautifulSoup(resp.text, "html.parser")

        # 查找包含 .flac 的链接
        # 方法1: 直接查找 href 包含 .flac 的 a 标签
        flac_a = page_soup.find("a", href=lambda href: href and ".flac" in href.lower())
        # 方法2: 如果方法1未找到，尝试查找文本包含 "FLAC" 的链接（更通用）
        if not flac_a:
            flac_a = page_soup.find("a", string=lambda s: s and "flac" in s.lower())
        # 方法3: 根据示例，FLAC链接在带有 class="songDownloadLink" 的 span 内的 a 标签中
        if not flac_a:
            span = page_soup.find("span", class_="songDownloadLink")
            if span:
                flac_a = span.find("a")

        if flac_a and flac_a.get("href"):
            flac_url = flac_a["href"]
            flac_links.append(flac_url)
            print(f"  找到FLAC: {flac_url}")
        else:
            print(f"  未找到FLAC链接")

        # 礼貌性延迟，避免对服务器造成压力
        time.sleep(1)
    if failed_logs:
        with open("failed_logs.txt", "w", encoding="utf-8") as f:
            for flog in failed_logs:
                f.write(flog + "\n")

            print(f"\n已将失败链接保存到 failed_logs.txt")
    return flac_links


def main():
    if len(sys.argv) < 2:
        print("用法: python script.py <初始页面URL>")
        sys.exit(1)

    initial_url = sys.argv[1]
    if initial_url.endswith("/"):
        initial_url = initial_url[:-1]
    flac_links = fetch_flac_links(initial_url)

    if flac_links:
        print("\n所有FLAC链接:")
        for link in flac_links:
            print(link)
        # 可选：保存到文件
        with open("flac_links.txt", "w", encoding="utf-8") as f:
            for link in flac_links:
                f.write(link + "\n")
        print(f"\n已将FLAC链接保存到 flac_links.txt")
    else:
        print("未提取到任何FLAC链接")


if __name__ == "__main__":
    main()
