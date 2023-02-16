# coding:utf-8
# writer:zhouyuhang
import os
import requests


headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}


def downLoad(url, filepath, size, ci):
    '''接受一个文件所在的url，将其稳定的写入filepath，如果文件大小小于size，则重新写入，最多为ci'''
    global res
    try:
        res = requests.get(url, headers=headers)
        if res.status_code != 200:
            for i in range(ci):
                print('请求错误，正在重新发起请求。。')
                res = requests.get(url, headers=headers)
                if res.status_code == 200:
                    break
                else:
                    continue
    except Exception as e:
        print('url无法请求!')

    # 下载
    f = open(filepath, 'wb')
    f.write(res.content)
    f_stat = os.stat(filepath)
    if f_stat.st_size < size:
        print('发现异常图片{}，正在重新下载。。'.format(url))
        for i in range(ci):
            f.write(res.content)
            f_stat = os.stat(filepath)
            if f_stat.st_size > size:
                break
            else:
                continue
    f.close()


downLoad('https://img.997pp.com/Tu/202203/4d9df7986d41c48884121d35690357ad.jpg',
         'D:/pythonjpgs/chai/doit.jpg',
         1000, 5)
