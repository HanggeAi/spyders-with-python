from utils.soupmaker import soup_maker
import requests

soup = soup_maker("https://xkcd.com/")
comelem = soup.select("#comic img")

if comelem == []:
    print("could not find any commic!")
else:
    comicurl = "https:" + comelem[0].get("src")
    imgfile = open("D:/pythonProject/pythonProject/爬虫虫/comic1.png", "wb")
    res = requests.get(comicurl)
    try:
        for chunk in res.iter_content(10000):
            imgfile.write(chunk)

    except:
        print("写入失败。。。")
