import asyncio
from pathlib import Path
from playwright.async_api import async_playwright, Route
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
import re
import sys


def download_file_as_string(url):
    print("正在获取 ", url, " 对应的文件")
    try:
        # 发送GET请求
        response = requests.get(url, timeout=30)

        # 检查响应状态
        response.raise_for_status()

        # 返回内容
        return response.text

    except requests.exceptions.RequestException as e:
        print(f"下载失败: {e}")
        return None


TARGET_M3U8 = "cmaf.m3u8"  # can only get camf.m3u8


async def intercept_and_get_m3u8_url(wwdc_video_url):
    """启动浏览器，拦截 prog_index.m3u8 请求并获取其 URL。"""

    # 使用 async_playwright 启动 Playwright
    async with async_playwright() as p:
        # 启动 Chromium 浏览器
        browser = await p.chromium.launch(headless=True)  # 可以设置为 True 在后台运行
        page = await browser.new_page()

        m3u8_url = None

        # 定义一个异步的路由拦截函数
        async def handle_route(route: Route):
            nonlocal m3u8_url
            url = route.request.url

            # 检查请求的 URL 是否包含目标文件名
            if TARGET_M3U8 in url:
                print(f"✅ 成功拦截到目标 M3U8 请求！")
                m3u8_url = url
                # 允许请求继续进行，但我们已经得到了 URL
                await route.continue_()
            else:
                # 其他请求，正常放行
                await route.continue_()

        # 启用路由拦截
        # Playwright 会检查所有发出的请求是否匹配 '*' 通配符
        await page.route("**/*", handle_route)

        print(f"🌐 正在访问 WWDC 视频页面: {wwdc_video_url}")

        try:
            # 访问页面，会触发网络请求，路由拦截函数会被调用
            await page.goto(wwdc_video_url, wait_until="networkidle")

            # 这里的页面加载时间可能不足以加载所有资源（包括字幕）。
            # 考虑等待一段时间，或者等待特定的网络响应。
            # 另一种更简单的方式是：等待直到 m3u8_url 被找到
            i = 0
            while i < 20:
                if m3u8_url:
                    break
                if i == 19:
                    isStop = input(
                        "It seems that network is not good, do you want to stop now? (Press Y to stop, other to continue.)")
                    try:
                        if str(isStop).lower == "y":
                            break
                        else:
                            i = 0
                    except Exception as e:
                        print("get error: ", e)
                    finally:
                        i = 0
                i += 1
                await asyncio.sleep(0.5)

        except Exception as e:
            print(f"⚠️ 页面加载时发生错误: {e}")

        finally:
            # 关闭浏览器
            await browser.close()

        return m3u8_url


async def get_base_url(wwdc_video_url):
    final_m3u8_url = await intercept_and_get_m3u8_url(wwdc_video_url)
    if final_m3u8_url:
        # example:
        # https://devstreaming-cdn.apple.com/videos/wwdc/2024/10168/4/D8EBB581-CA62-4601-A3DF-BCF4C7805EBE/cmaf.m3u8?18665
        return final_m3u8_url.rsplit("/", 1)[0]
    print("❌ 未找到 base URL。")
    return None


def get_all_webvtt_content_from(index_file_content):
    return re.findall("sequence.*.webvtt", index_file_content)


def download_subtitle(subtitle_url, save_file):
    url = subtitle_url
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_file, "wb") as file:
            file.write(response.content)
        print(f"Downloaded {save_file}")
        return True
    else:
        print(f"Failed to download {save_file}")
        return False


async def download_webvtts(base_url, webvtt_itmes):
    print("尝试下载 ", len(webvtt_itmes), " 个 webvtt 文件，请稍后")
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(download_subtitle, base_url + item, item)
                   for item in webvtt_itmes]
        for future in as_completed(futures):
            future.result()


async def get_webvtt_file_from(wwdc_video_url, output_file_name):
    base_url = await get_base_url(wwdc_video_url)
    if base_url:
        base_url = base_url + "/subtitles/eng/"
        index_url = base_url + "prog_index.m3u8"
        print("下载 prob_index 文件")
        file_content = download_file_as_string(index_url)
        if file_content:
            all_webvtt_items = get_all_webvtt_content_from(file_content)
            await download_webvtts(base_url, all_webvtt_items)
            merge_and_clean_subtitles(all_webvtt_items, output_file_name)


def merge_and_clean_subtitles(all_webvtt_file_path, output_file_name):
    print("正在合并多个 webvtt 文件 到 srt，请稍后...")
    current_cnt = 1
    with open(output_file_name, "w", encoding='utf-8') as full_file:
        for webvtt in all_webvtt_file_path:
            with open(webvtt, "r", encoding='utf-8') as file:
                content = file.read()
                # Remove timestamp lines, WEBVTT tags, and extra blank lines
                cleaned_content = re.sub(r'(WEBVTT)\n', '', content)
                # Replace multiple consecutive newlines with a single newline
                cleaned_content = re.sub(r'\n\s*\n', '\n', cleaned_content)
                # if file content do not contains xx:xx:xx.xxx --> xx:xx:xx.xxx, ignore it
                if len(cleaned_content) < 29:
                    continue
                full_file.write(f"{current_cnt}" + cleaned_content + "\n")
                current_cnt += 1
            print(f"Merged {webvtt}")
        is_remove_cache = input("合并完成，是否删除所有 webvtt 缓存文件？[Y/Other keys]")
        if is_remove_cache == "y" or is_remove_cache == "Y":
            for webvtt_file in Path(".").glob("**/*.webvtt"):
                try:
                    webvtt_file.unlink()  # 删除文件
                    print(f"已删除: {webvtt_file}")
                except Exception as e:
                    print(f"删除失败 {webvtt_file}: {e}")


def printHelp():
    print(
        """
使用方法：python wwdcSubTtileDownloader.py <https://wwdc/video/url>
例如：python wwdcSubTitleDownloader.py https://developer.apple.com/videos/play/wwdc2024/10168/
"""
    )


def may_valid_wwdc_url(wwdc_url):
    return type(wwdc_url) == str and str(wwdc_url).startswith("https://developer.apple.com/videos/play/") and get_file_name(wwdc_url) != None


def get_file_name(wwdc_url):
    pattern1 = r'wwdc(\d{4})/(\d+)'
    video_num_re_ret = re.findall(pattern1, wwdc_url)
    if type(video_num_re_ret) == list and len(video_num_re_ret) > 0 and type(video_num_re_ret[0]) == tuple and len(video_num_re_ret[0]) > 1:
        return f"wwdc{video_num_re_ret[0][0]}-{video_num_re_ret[0][1]}.srt"
    return None


if __name__ == "__main__":
    if len(sys.argv) > 1:
        wwdc_url = sys.argv[1]
        if may_valid_wwdc_url(wwdc_url):
            asyncio.run(get_webvtt_file_from(
                wwdc_url, get_file_name(wwdc_url)))
            exit(0)
    print("❌ 参数错误或 url 不正确，请检查")
    printHelp()
