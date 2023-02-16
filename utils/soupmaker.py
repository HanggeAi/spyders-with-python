import requests
from bs4 import BeautifulSoup


def soup_maker(url1: str):
    """接受一个url，返回一锅汤"""
    try:
        res = requests.get(url1)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
    except Exception as e:
        soup = BeautifulSoup('<a>text</a>')
    return soup
