import requests
from bs4 import BeautifulSoup
import openpyxl
from utils.soupmaker import soup_maker  # 直接调用函数


def book_info(url):
    info_list = []
    info_dict = {}
    soup = soup_maker(url)
    span_list = soup.find_all('span')
    for ele in span_list:
        if ele.text != '' and '：' in ele.text:
            # print(type(ele.text))
            ele.text.replace('xa0', '')
            ele.text.replace(' ', '')  # 去除空格
            # print(ele.text)
            info_list.append(ele.text)
            new_list = info_list[1:9]

    return new_list


# url='https://www.phei.com.cn/module/goods/wssd_content.jsp?bookid=59693'
# print(book_info(url))


def get_intro(url):
    """获得每本书的介绍文字，url是对应于每本书的"""
    soup = soup_maker(url)
    tp = soup.find_all('p')
    for p in tp:
        if len(p.text) > 100:
            st = p.text
        else:
            st = '未找到介绍信息'
    return st


def get_book_url():
    """获得每一本书的专属url"""
    urls = []
    book_url_list = []
    final_book_url_list = []
    for i in range(1, 4):
        urls.append('https://www.phei.com.cn/module/goods/searchkey.jsp?Page='
                    + str(i) + '&searchKey=%E8%AE%A1%E7%AE%97%E6%9C%BA')
    for url in urls:
        soup = soup_maker(url)
        a_list = soup.find_all('a')  # 每一页中，找到中多书href所在的a标签
        for a in a_list:
            if 'jsp?bookid=' in a.attrs['href'] and 'https' not in a.attrs['href']:
                if '{' not in a.attrs['href']:
                    book_url = 'https://www.phei.com.cn' + a.attrs['href']  # 最终合理的url

                    book_url_list.append(book_url)
    final_book_url_list = book_url_list[0:len(book_url_list):2]
    return final_book_url_list


def get_book_name(url):
    """根据url，爬取书的名字"""
    soup = soup_maker(url)
    h = soup.find_all('h1')
    name = h[0].text.replace('\xa0', '')
    return name


def main():
    """主函数"""

    wb = openpyxl.Workbook()
    ws = wb.create_sheet('书的各项信息')
    count = 1
    url_list = get_book_url()
    for url in url_list:
        book_row = []  # 每本书的一行，作为一个列表
        b_name = get_book_name(url)
        book_row.append(b_name)
        b_info = book_info(url)
        for ele in b_info:
            book_row.append(ele)
        b_intro = get_intro(url)
        book_row.append(b_intro)
        ws.append(book_row)
        print('第%s本书录入完成！' % count)
        count += 1
    wb.save(filename='com_book_info.xlsx')


if __name__ == "__main__":
    main()
