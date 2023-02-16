from urllib.parse import urlencode
import requests

base_url = "https://m.weibo.cn/api/container/getIndex?"
from pyquery import PyQuery as pq

headers = {
    "Host": "m.weibo.cn",
    "Referer": "https://m.weibo.cn/u/283678474",
    "User_Agent": "Mozilla/5.0(Macintosh;Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML,like Gecko)"
                  "Chrome/58.0.3029.110 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
}


def get_page(page):
    params = {
        "type": "uid",
        "value": "2830678474",
        "containerid": "1076032830678474",
        "page": page
    }
    url = base_url + urlencode(params)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError as e:
        print("error!!", e.args)


def parse_page(json):
    """解析json,实际上就是解析字典"""
    if json:
        """如果json不为空值"""
        items = json.get("data").get("cards")
        for item in items:
            item = item.get("mblog")
            weibo = {}
            weibo["id"] = item.get("id")
            weibo["text"] = item.get("raw_text")
            weibo["attitudes"] = item.get("attitudes_count")
            weibo["comments"] = item.get("comments_count")
            weibo["resposts"] = item.get("reposts_count")
            yield weibo  # 返回weibo 生成器


if __name__ == "__main__":
    for page in range(1, 11):
        json = get_page(page)
        results = parse_page(json)
        for result in results:
            print(result)
