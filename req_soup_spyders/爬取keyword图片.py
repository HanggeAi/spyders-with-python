import os, requests, time
from utils.soupmaker import soup_maker

ori_url = "https://www.toutiao.com/fengjing"
o_url = "https://www.toutiao.com"


def get_url1(url):
    """接受原始url，返回每一个相册的url"""
    list1 = []
    soup = soup_maker(url)
    dts = soup.find_all("dt")
    for dt in dts:
        if "title" in dt.a.attrs:
            # print(dt.a.get("href"))
            url1 = o_url + dt.a.get("href")
            list1.append(url1)
            print("相册链接：", url1)
    return list1


def get_url2(urlist):
    """接受相框链接列表，返回相框中每张图片的url的list"""
    ff = open("D:/pythonjpgs/grils/gril.txt", "w")
    global im_href
    final_url = []
    for url in urlist:
        soup1 = soup_maker(url)
        img = soup1.find_all("img")
        for im in img:
            try:
                im_href = im.get("src")
                final_url.append(im_href)
                print("图片地址： " + im_href)
                ff.write(im_href + "\n")
            except:
                for i in range(10):
                    im_href = im.get("src")
                    if im_href != None:
                        pass
                    else:
                        continue
            final_url.append(im_href)
    ff.close()
    return final_url


def save_img(im_url_list):
    """接受每一个图片的url，将其保存到本地"""

    for url in im_url_list:
        image_file = open(os.path.join("D:/pythonjpgs/grils/", os.path.basename(url)), "wb")
        ress = requests.get(url)
        for chunk in ress.iter_content(100000):
            image_file.write(chunk)
        image_file.close()
        time.sleep(1)


if __name__ == "main":
    list1 = get_url1(ori_url)
    list2 = get_url2(list1)
    save_img(list2)
