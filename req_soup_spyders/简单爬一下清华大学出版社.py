from utils.soupmaker import soup_maker

url = "http://www.tup.tsinghua.edu.cn/booksCenter/booklist.html?keyword=python&keytm=8E38392C948E9C6C8C"
soup = soup_maker(url)
ts = soup.find_all("span")
for i in ts:
    if "title" in i.attrs.keys():
        print(i.text)
