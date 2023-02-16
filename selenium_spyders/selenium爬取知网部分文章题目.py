from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.support.wait import WebDriverWait
import time

url = 'https://www.cnki.net'
driver = webdriver.Chrome()
driver.get(url)


def get_now_page_content():
    """获取当前页面的内容"""
    time.sleep(2)  # 等待浏览器完全加载完毕

    s = driver.page_source
    print('已经得到渲染后的网页源代码，长度为%s' % (len(s)))
    soup = BeautifulSoup(s, 'html.parser')
    tr = soup.find_all('tr')
    print(len(tr))
    try:
        for t in tr[1:]:
            # print(t.a.text)
            au = t.select('td[class="author"]')
            # print(au)
            date = t.select('td[class="date"]')
            # print(date)
            source = t.select('td[class="source"]')
            # print(source)
            a_list = []
            for na in au[0].find_all('a'):
                a_list.append(na.text)
            dict = {
                'title': t.a.text,
                'author': a_list,
                'date': date[0].text,
                'source': source[0].a.text,
            }
            print(dict)
    except Exception as ec:
        print('soupError')
    # return dict


def next_page():
    """模拟点击翻页"""
    next_btn = driver.find_element(By.ID, 'PageNext')
    next_btn.click()


def main(word):
    """先搜索要搜索的词"""
    Input = driver.find_element(By.ID, 'txt_SearchText')  # 输入框(sb知网居然连这个都变化！)
    Input.send_keys(word)  # 注意这里的Input是一个长度为1的列表，因为上面是elements
    button = driver.find_element(By.CLASS_NAME, 'search-btn')  # 搜索按钮
    button.click()

    # 取得当前页的内容
    get_now_page_content()
    time.sleep(2)
    next_page()


if __name__ == "__main__":
    main('TBM')
