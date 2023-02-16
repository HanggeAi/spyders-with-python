# coding:utf-8
# writer:zhouyuhang
from selenium import webdriver
import time, os, requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
ori_url = "https://www.taobao.com"
driver = webdriver.Chrome(options=options)
driver.get(ori_url)
driver.maximize_window()  # 窗口最大化
wait1 = WebDriverWait(driver, 8)  # 8秒的等待对象


def search(keyword):
    """找到搜索框，然后搜索"""
    input = wait1.until(EC.presence_of_element_located((By.ID, "q")))
    input.send_keys(keyword + "\n")  # 直接采用回车键
    time.sleep(8)  # 手动扫码登录
    all_goods = wait1.until(EC.presence_of_element_located((By.ID, "tabFilterAll")))  # 等待所有元素加载完毕


def get_now_urls(url_type="taobao"):
    """获取当前页面所有商品的url,
    但是应注意，所获得的url中，有的是天猫链接，有的是淘宝链接，
    二者的解析方法不一样。"""
    urls = []
    urls_taobao = []
    urls_tianmao = []
    driver.minimize_window()  # 窗口最小化
    page_source = driver.page_source
    soup = BeautifulSoup(page_source)
    a = soup.find_all("a", {"class": "pic-link J_ClickStat J_ItemPicA"})
    for aa in a:
        if "https:" not in aa.get("href"):
            urls.append("https:" + aa.get("href"))
        else:
            urls.append(aa.get("href"))
    for url in urls:
        if "item.taobao" in url:
            urls_taobao.append(url)
        else:
            urls_tianmao.append(url)

    print("得到%s个商品url" % len(urls))
    print("其中淘宝商品链接个数: ", len(urls_taobao))
    print("其中天猫商品链接个数: ", len(urls_tianmao))
    if url_type == "taobao":
        return urls_taobao
    if url_type == "tianmao":
        return urls_tianmao


def get_taobao_info_by_driver(url_list):
    """接受商品url列表，返回其中感兴趣的信息"""
    info = []
    for url in url_list:
        dic = {}
        dic["url"] = url
        driver.get(url)
        time.sleep(3)
        text = driver.page_source
        soup = BeautifulSoup(text)
        div1 = soup.select("div[id='J_Title']")[0]
        h3 = div1.find("h3")
        dic["title"] = h3.text
        class_inf = soup.find("div", {"id": "J_isku"})
        lis = class_inf.find_all("li")
        dic["颜色分类"] = []
        for li in lis:
            span = li.find("span")
            dic["颜色分类"].append(span.text)
        info.append(dic)

    return info


def get_tmall_info_by_driver(url_list):
    """接受商品url列表，返回其中感兴趣的信息"""
    info = []
    for url in url_list:
        dic = {}
        intrest = []
        dic["url"] = url
        driver.get(url)
        time.sleep(2)  # 不能连续访问，需要休息一下
        time.sleep(0.1)  # 等待浏览器加载页面完成
        text = driver.page_source
        soup = BeautifulSoup(text, "html.parser")
        div1 = soup.find("div", {"class": "tb-detail-hd"})
        t = div1.find("h1")
        dic["title"] = t.text.replace("\t", "").replace("\n", "")
        try:
            classfy_tag = soup.find("div", {"class": "tb-key"})
        except:
            classfy_tag = soup.find("div", {"id": "J_isku"})

        lis = classfy_tag.find_all("li")
        for li in lis:
            if li.get("title") != None:
                intrest.append(li.get("title"))
        dic["颜色分类"] = intrest
        info.append(dic)
    return info


if __name__ == "__main__":
    search("达尔优键盘")
    urlls = get_now_urls("taobao")
    for u in urlls:
        print(u)
    inf1 = get_taobao_info_by_driver(urlls[:5])
    print(inf1)
    time.sleep(1)
    driver.close()
    dff = pd.DataFrame(inf1)
    dff.to_excel("D:/pythonjpgs/taobao_data1.xlsx")

# 下一步优化：只需将增加一个翻页功能，将每一页得到的url列表组合成一个打的url列表
# 再继续使用解析函数即可。
# 使用.extend方法即可
