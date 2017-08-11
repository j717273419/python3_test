# coding=utf-8
# 需要先安装pip install beautifulsoup4
from urllib.request import *
from bs4 import BeautifulSoup
import re
import time
import random
import socket

url = "http://pic.sogou.com/pics?query=%B1%DA%D6%BD&di=2&_asf=pic.sogou.com&w=05009900&sut=3086&sst0=1492360460259";

html = urlopen(url)
obj = BeautifulSoup(html,"html.parser")
randomBeginIndex = random.randint(2,5)

urls = re.findall(r'"pic_url":"(.*?)"',str(obj))
for picAddress in urls:
    if randomBeginIndex < 50:
        print("开始从第 %d 张图片下载" % randomBeginIndex)
        randomSleepSeconds = random.randint(3, 10)
        print("休息 %d 秒，不要被网站捉到喔！" % randomSleepSeconds)
        time.sleep(randomSleepSeconds)
        try:

            picUrl = picAddress.replace('\\','')
            #title = re.sub(r'<\\?\\?/?\w+[^>]*>','',picAddress[1])
            print("图片地址是 %s" % (picUrl))
            socket.setdefaulttimeout(20)
            urlretrieve(picUrl, "WallPaper/sogou_"+str(randomBeginIndex) + ".Png")
            print("成功下载第%d张图片" % randomBeginIndex)
        except:
            print("发生异常在下载第"+str(randomBeginIndex)+"张图片时。")
            continue
        randomBeginIndex = randomBeginIndex + 1

print("全部图片下载成功，共下载 %d 张图片" % randomBeginIndex)

