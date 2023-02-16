# coding:utf-8
# writer:zhouyuhang
from selenium import webdriver
import os, time, requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os.path as op
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from hanzi_panduan import *
import openpyxl

driver = webdriver.Chrome()
ori_url = "https://search.bilibili.com/all?vt=86646923&keyword="


def search(keyword):
    """输入要搜索的视频名称，返回搜索界面源代码"""

    sear_url = ori_url + keyword
    driver.get(sear_url)
    driver.maximize_window()  # 窗口最大化
    wait1 = WebDriverWait(driver, 8)  # webdriverwait对象

    time.sleep(3)
    text = driver.page_source  # 为什么得到的总是首页的源代码？？？？
    f = open(os.getcwd() + os.sep + "bili.html", "w", encoding="utf-8")
    f.write(text)
    f.close()
    print(len(text))
    return text


def get_each_url(text):
    """接受网页的源代码，从中get所有结果视频的url"""
    video_url = []
    final_urls = []
    soup = BeautifulSoup(text, "html.parser")
    big_div = soup.find_all("div", {"class": "video-list row"})
    sub_div = big_div[0].find_all("div")  # 问题应该是出现在这里

    for d in sub_div:
        # print(d.get("class"))
        a = d.find("a")
        if a != None:
            video_url.append(a.get("href"))
    sett = set(video_url)
    flist = list(sett)
    for i in flist:
        furl = i.replace("//", "https://")
        print(furl)
        final_urls.append(furl)
    # for l in final_list:
    #     print(l)

    return final_urls


def soup_find(a_res):
    """接受一个res，然后信息字典"""
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
    # tag_fans = soup.select("#v_upinfo > div.up-info_right > div.btn-panel")
    # fans = tag_fans[0].find("span").find("span").text
    dict = {}  # 用于存放信息的空字典
    dict["标题"] = title
    dict["播放量"] = han_except(viewCount)
    dict["点赞"] = han_except(like)
    dict["投币数"] = han_except(coin)
    dict["弹幕"] = han_except(danmu)
    dict["up主"] = name
    # dict["up主粉丝"] = han_except(fans)
    dict["日期"] = date
    return dict


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE"
}


def parse_each_page(url):
    """接受一个url,返回该url对应的相关信息"""

    a_res = requests.get(url, headers=headers)  # 具体视频界面的url中，我们所需要的信息不再是js动态渲染的了，这十分方便。
    if a_res.status_code != 200:
        for i in range(30):  # 重试三次
            a_res = requests.get(url, headers=headers)
            if a_res.status_code != 200:
                continue
            else:
                break
    print("状态码： ", a_res.status_code)
    return a_res


def dict2list(di):
    """将信息写入表格"""
    list = []
    for value in di.values():
        list.append(value)

    return list


def next_page(keyword, page_num):
    """翻页操作"""
    next_url1 = "https://search.bilibili.com/all?keyword="
    next_url2 = "&from_source=webtop_search&spm_id_from=333.1007&page="
    next_url = next_url1 + keyword + next_url2 + str(page_num) + "&o=24"
    print("next url is: ", next_url)
    driver.get(next_url)
    print("等待3秒加载源码。。")
    time.sleep(3)  # 等待页面加载完全
    f = open(os.getcwd() + os.sep + "bili_next.txt", "wb")
    f.write(driver.page_source.encode())
    f.close()
    return driver.page_source


def f_main(sheet, keyword):
    """伪主函数"""
    page_text = search(keyword)
    uurl_list = get_each_url(page_text)

    for url in uurl_list:
        try:
            dictt = soup_find(parse_each_page(url))
            list1 = dict2list(dictt)
            sheet.append(list1)
            print(url, " 的信息录入成功。")
        except AttributeError:
            print(url, " 的信息录入失败。。")
            pass


def real_main(n, kw):
    """真主函数"""
    # 写入表格

    wb = openpyxl.Workbook()
    sheet = wb.active
    if n < 2:
        f_main(sheet, kw)

    else:
        f_main(sheet, kw)
        for i in range(2, n + 1):
            tt = next_page(kw, i)
            urllist = get_each_url(tt)
            for url in urllist:
                try:
                    dictt = soup_find(parse_each_page(url))
                    list1 = dict2list(dictt)
                    sheet.append(list1)
                    print(url, " 的信息录入成功。")
                except AttributeError:
                    print(url, " 的信息录入失败。。")
                    pass
    wb.save(filename="D:/pythonjpgs/bili.xlsx")
    wb.close()


if __name__ == "__main__":
    real_main(10, "python爬虫")

# 在本次程序中遇到的问题及其解决办法：
# 问题1：selenium翻页得不到源代码，而是首页的代码
# 解决办法： 利用url中的page翻页

# 问题2： 对于有的视频url,会出现soup不完整的情况
# 解决办法： 1、加上请求头 2、多get几次

# 问题3： 对于视频列表的上一级div，如果使用右键复制css selector 翻页之后由于元素变化，找不到此big_div
# 解决办法： 使用find_all("div",{"class":""}) 来寻找此bing_div
