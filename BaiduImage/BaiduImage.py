# coding=utf-8
# 需要先安装pip install beautifulsoup4
from urllib.request import *
from bs4 import BeautifulSoup
import re

url = 'https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1492334463206_R&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&word=%E6%90%9E%E7%AC%91+gif'
html = urlopen(url)
obj = BeautifulSoup(html,'html.parser')
index = 0
urls = re.findall(r'"objURL":"(.*?)"',str(obj))
for url in urls:
    if index < 100:
        try:
            urlretrieve(url,'pic'+str(index)+'.png')
            index +=1
        except Exception:
            print ('下载失败 第%d张图片' % index)
    else:
        print('下载完成')
        break
