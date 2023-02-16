# coding:utf-8
# writer:zhouyuhang
import os

from selenium import webdriver
import time
import requests
from bs4 import BeautifulSoup
# 动态爬虫中，基本上是用不到soupmaker，因为其接受的也是一个url，只能用在静态小型爬虫中。
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os.path as op
from selenium.common.exceptions import TimeoutException, NoSuchElementException

ori_url = "https://www.taobao.com/"
driver = webdriver.Chrome()
driver.get(ori_url)
driver.maximize_window()  # 窗口最大化
wait1 = WebDriverWait(driver, 8)  # webdriverwait对象


# input1=driver.find_element(By.ID,"q")
# print(type(input1))
# input2=wait1.until(EC.presence_of_element_located((By.ID,"q")))
# print(type(input2))
# print(input2==input1)
def search(key_word):
    """找到搜索框，点击搜索"""
    input = wait1.until(EC.presence_of_element_located((By.ID, "q")))
    button = wait1.until(EC.presence_of_element_located((By.CLASS_NAME, "search-button")))
    input.send_keys(key_word)
    time.sleep(0.5)
    button.click()
    time.sleep(8)  # 手动登录
    all_good = wait1.until(EC.presence_of_element_located((By.ID, "tabFilterAll")))


def get_now_urls():
    """获取当前页面的所有宝贝图片的url"""
    url_list = []
    url_list1 = []
    url_list2 = []
    time.sleep(2)
    text = driver.page_source
    print(len(text))
    file = open("taobao.html", "wb")
    file.write(text.encode())
    file.close()
    soup = BeautifulSoup(text)
    img = soup.find_all("img", {"class": "J_ItemPic img"})
    print(len(img))
    for im in img:
        ii = im.get("data-src")
        # print(ii)
        if "http" in ii:
            url_list2.append(ii)
        else:
            url_list1.append(ii)
    for url in url_list1:
        if "http" not in url:
            url = "http:" + url
            url_list.append(url)
    return url_list + url_list2


def next_page():
    """跳转到下一页，为获得接下来的源代码做准备"""
    try:
        next_page = WebDriverWait(driver, 3, 0.2).until(
            lambda x: x.find_element_by_xpath("//span[contains(text(),'下一页')]/.."))  # 包含文本内容的span元素
    except Exception as e:
        print(e)

    else:
        next_page.click()


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE"
}


def save_img(ulist):
    """传入一个url列表，将每一个url储存到本地"""
    for url in ulist:
        res = requests.get(url, headers=headers)
        f = open(op.join("D:/pythonjpgs/pants", op.basename(url)), "wb")
        f.write(res.content)
        f_stat = os.stat(op.join("D:/pythonjpgs/pants", op.basename(url)))
        if f_stat.st_size < 1000:  # 字节数小于1000说明没有保存成功
            print("发现异常图片{}，正在重新下载。。".format(url))
            for i in range(3):  # 事不过三
                r_res = requests.get(url)  # 有的时候图片会写入失败，可以多请求几次，会发现成功了。
                f = open(op.join("D:/pythonjpgs/pants", op.basename(url)), "wb")
                f.write(r_res.content)
                r_f_stat = os.stat(op.join("D:/pythonjpgs/pants", op.basename(url)))
                if r_f_stat.st_size > 1000:  # 如果满足大小条件，则跳出循环
                    print("重新下载成功！")
                    break
                else:  # 不满足大小条件，就重新写入文件
                    print("重新下载未果。。")
                    continue
        f.close()
        print(op.basename(url) + "已保存")
        time.sleep(1)


def main(n):
    """n页数"""
    search("牛仔裤 男士")
    time.sleep(2)
    for i in range(n):
        url_list = get_now_urls()
        save_img(url_list)
        next_page()


if __name__ == "__main__":
    main(50)  # 两页
    driver.quit()  # 退出浏览器，不留任何痕迹。
