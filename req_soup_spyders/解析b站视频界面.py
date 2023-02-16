# coding:utf-8
# writer:zhouyuhang
import requests
from bs4 import BeautifulSoup
from hanzi_panduan import *
import openpyxl


def parse_each_page(url):
    """接受一个url,返回该url对应的相关信息"""
    dict = {}  # 用于存放信息的空字典
    a_res = requests.get(url)  # 具体视频界面的url中，我们所需要的信息不再是js动态渲染的了，这十分方便。
    if a_res.status_code != 200:
        for i in range(3):  # 重试三次
            a_res = requests.get(url)
            if a_res.status_code != 200:
                continue
            else:
                break

    soup = BeautifulSoup(a_res.text, "html.parser")
    tag_title = soup.find("h1", {"class": "video-title"})
    title = tag_title.get("title")  # 视频标题
    tag_viewCount = soup.find("span", {"class": "view"})
    viewCount = tag_viewCount.get("title")  # 视频播放量
    tag_like = soup.find("span", {"class": "like"})
    like = tag_like.get("title")  # 点赞
    tag_coin = soup.find("span", {"class": "coin"})
    coin = tag_coin.get("title")  # 投币
    tag_danmu = soup.find("span", {"class": "dm"})
    danmu = tag_danmu.get("title")
    tag_date = soup.select("#viewbox_report > div > span:nth-child(3)")
    date = tag_date[0].text
    tag_name = soup.find("div", {"class": "name"})
    namea = tag_name.find("a")
    name = namea.text.replace(" ", "").replace("\n", "")
    tag_fans = soup.select("#v_upinfo > div.up-info_right > div.btn-panel > div > span > span")
    fans = tag_fans[0].text
    dict["标题"] = title
    dict["播放量"] = han_except(viewCount)
    dict["点赞"] = han_except(like)
    dict["投币数"] = han_except(coin)
    dict["弹幕"] = han_except(danmu)
    dict["up主"] = name
    dict["up主粉丝"] = han_except(fans)
    dict["日期"] = date
    return dict


try:
    d = parse_each_page("https://www.bilibili.com/video/BV1jE411T7ya")
    print(d)
except IndexError as e:
    print("list out of range")

list = []
for value in d.values():
    list.append(value)

print(list)
wb = openpyxl.Workbook()
sheet = wb.active
sheet.append(list)
wb.save(filename="D:/pythonjpgs/bili.xlsx")
