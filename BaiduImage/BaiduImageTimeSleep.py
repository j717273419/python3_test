# coding=utf-8
# 需要先安装pip install beautifulsoup4
from urllib.request import *
from bs4 import BeautifulSoup
import re
import time
import random

url = "https://image.baidu.com/search/index?ct=201326592&cl=2&st=-1&lm=-1&nc=1&ie=utf-8&tn=baiduimage&ipn=r&rps=1&pv=&fm=rs10&word=%E5%BC%A0%E9%9B%AA%E8%BF%8E&oriquery=%E6%9E%97%E5%85%81&ofr=%E6%9E%97%E5%85%81";

html = urlopen(url)
obj = BeautifulSoup(html,"html.parser")
randomBeginIndex = random.randint(1,5)

urls = re.findall(r'"objURL":"(.*?)"',str(obj))
for picAddress in urls:
    if randomBeginIndex < 100:
        print("开始从第 %d 张图片下载" % randomBeginIndex)
        randomSleepSeconds = random.randint(5, 10)
        print("休息 %d 秒，不要被网站捉到喔！" % randomSleepSeconds)
        time.sleep(randomSleepSeconds)
        try:
            urlretrieve(picAddress,str(randomBeginIndex)+".Png")
            print("成功下载第%d张图片" % randomBeginIndex)
        except:
            print("发生异常在下载第"+str(randomBeginIndex)+"张图片时。")
            break
        randomBeginIndex = randomBeginIndex + 1

print("全部图片下载成功，共下载 %d 张图片" % randomBeginIndex)
