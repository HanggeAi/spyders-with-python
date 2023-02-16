# coding:utf-8
# writer:zhouyuhang
import requests
from bs4 import BeautifulSoup

url = "https://tieba.baidu.com/home/main?id=tb.1.527654d3.naRsp70LOxNARCD-duS28g?t=1626109140&fr=pb"
headers = {"User-Agent":
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"}
res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.text)
ties = soup.find_all("div", {"class": "thread_name"})
true_url_list = []  # 存放各个帖子的真实url
for tie in ties:
    tie_href = tie.find("a")  # 帖子的url所在标签
    tie_url = tie_href.get("href")  # 帖子链接
    # print(tie_url)
    true_url_list.append("https://tieba.baidu.com/" + tie_url)

for url in true_url_list:
    res2 = requests.get(url, headers=headers)
    soup2 = BeautifulSoup(res2.text)
    img2 = soup2.find_all("img", {"class": "BDE_Image"})

    for im in img2:
        src = im.get("src")  # 每张图片的真实地址
        im_res = requests.get(src, headers=headers)
        with open("D:/pythonjpgs/爬虫/shufa/" + src[-15:-1] + ".jpg", "wb") as f:
            f.write(im_res.content)
        print(src[-15:-1] + "保存成功。")
