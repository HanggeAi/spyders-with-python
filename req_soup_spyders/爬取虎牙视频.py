# coding:utf-8
# writer:zhouyuhang
import requests
import re

v_url = "https://liveapi.huya.com/moment/getMomentContent?videoId=524694291"  # 某一个特定视频的url，注意，这里删去了

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"}

# 获取特定视频的部分信息：
# res1=requests.get(v_url,headers=headers)
# title=res1.json()["data"]["moment"]["title"]
# url=res1.json()["data"]["moment"]["videoInfo"]["definitions"][0]["url"] # 原画画质的url链接
#
# with open("D:/pythonjpgs/爬虫/"+title+".mp4","wb") as f:
#     f.write(requests.get(url).content)
#     print(title+"was saved successfully")

# 对于多个视频的爬取，需要多个v_url。这就需要获得多个视频的id。要获得多个视频的id可以从视频的列表页中获取。
# 幸运的是，这里的网页源代码中，直接就有各个视频的id！


def huyavideo(url):
    """传入一个响应为json的url，解析其标题和视频原画地址，然后保存"""
    res1 = requests.get(url, headers=headers)
    title = res1.json()["data"]["moment"]["title"]
    url11 = res1.json()["data"]["moment"]["videoInfo"]["definitions"][0]["url"]  # 原画画质的url链接

    with open("D:/pythonjpgs/爬虫/" + title + ".mp4", "wb") as f:
        f.write(requests.get(url11).content)
        print(title + " was saved successfully")


url_list = ["https://liveapi.huya.com/moment/getMomentContent?videoId=" + id for id in id_list]


# for urlii in url_list:
#     huyavideo(urlii)

def get_video_id(keyword, start, end):
    """通过所给搜索关键词keyword和始末页码start end,
    返回这些页面中所有视频id"""
    id_list_big = []
    for ii in range(start, end + 1):
        list_url = "https://v.huya.com/search?w=%s&type=video" % keyword + "&order=general&p=%s" % ii
        res22 = requests.get(list_url, headers=headers)
        id_list = re.findall("{'vid':(\d+)", res22.text)
        id_list_big.append(id_list)
    return id_list_big


def main(kw, s, e):
    """主函数"""
    mylist = get_video_id(kw, s, e)
    for page in mylist:
        for vd in page:
            final_url = "https://liveapi.huya.com/moment/getMomentContent?videoId=" + vd
            huyavideo(final_url)


import threading

t1 = threading.Thread(target=main, args=("csgo", 1, 5))
t2 = threading.Thread(target=main, args=("csgo", 5, 10))

t1.start()
t2.start()
