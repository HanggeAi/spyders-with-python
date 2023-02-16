import bs4, os, requests

url = "http://xkcd.com"  # 初始的url
os.makedirs("xkcd", exist_ok=True)

while not url.endswith("#"):  # URL 以"#"结束，你就知道需要结束循环
    print("downloading page %s" % url)
    res = requests.get(url)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text)
    comelem = soup.select("#comic img")  # 找出带有id属性为comic的元素，且img需要在comic之内
    if comelem == []:
        print("could not find any commic!")
    else:
        comicurl = "https:" + comelem[0].get("src")
        # 开始下载
        print("downloading image %s" % (comicurl))
        res = requests.get(comicurl)
        res.raise_for_status()
        # save images:
        iamgefile = open(os.path.join("xkcd", os.path.basename(comicurl)), "wb")
        for chunk in res.iter_content(10000):
            iamgefile.write(chunk)
        iamgefile.close()

        # get the prev button"s url
        prelink = soup.select("a[rel='prev']")[0]  # 选择器"a[rel="prev"]"识别出 rel 属性设置为 prev 的<a>元素
        url = "http://xkcd.com" + prelink.get("href")  # 更新url
