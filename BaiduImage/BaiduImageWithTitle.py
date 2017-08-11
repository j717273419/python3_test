# coding=utf-8
# 需要先安装pip install beautifulsoup4
from urllib.request import *
from bs4 import BeautifulSoup
import re
import time
import random
import socket

url = "https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=index&fr=&hs=0&xthttps=111111&sf=1&fmq=&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&word=%E5%A3%81%E7%BA%B8&oq=%E5%A3%81%E7%BA%B8&rsp=-1";

html = urlopen(url)
obj = BeautifulSoup(html,"html.parser")
randomBeginIndex = random.randint(2,5)

urls = re.findall(r'("objURL":".*?) "fromPageTitle":"(.*?)"',str(obj))
for picAddress in urls:
    if randomBeginIndex < 50:
        print("开始从第 %d 张图片下载" % randomBeginIndex)
        randomSleepSeconds = random.randint(3, 10)
        print("休息 %d 秒，不要被网站捉到喔！" % randomSleepSeconds)
        time.sleep(randomSleepSeconds)
        try:

            picUrl = re.findall(r'"objURL":"(.*?)"',picAddress[0])[0]
            title = re.sub(r'<\\?\\?/?\w+[^>]*>','',picAddress[1])
            print("图片地址是 %s,标题是 %s" % (picUrl,title))
            socket.setdefaulttimeout(20)
            urlretrieve(picUrl, "WallPaper/"+title + str(randomBeginIndex) + ".Png")
            print("成功下载第%d张图片" % randomBeginIndex)
        except:
            print("发生异常在下载第"+str(randomBeginIndex)+"张图片时。")
            continue
        randomBeginIndex = randomBeginIndex + 1

print("全部图片下载成功，共下载 %d 张图片" % randomBeginIndex)


##过滤HTML中的标签
#将HTML中标签等信息去掉
#@param htmlstr HTML字符串.
def filter_tags(htmlstr):
  #先过滤CDATA
  re_cdata=re.compile('//<!\[CDATA\[[^>]*//\]\]>',re.I) #匹配CDATA
  re_script=re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I)#Script
  re_style=re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>',re.I)#style
  re_br=re.compile('<br\s*?/?>')#处理换行
  re_h=re.compile('</?\w+[^>]*>')#HTML标签
  re_comment=re.compile('<!--[^>]*-->')#HTML注释
  s=re_cdata.sub('',htmlstr)#去掉CDATA
  s=re_script.sub('',s) #去掉SCRIPT
  s=re_style.sub('',s)#去掉style
  s=re_br.sub('\n',s)#将br转换为换行
  s=re_h.sub('',s) #去掉HTML 标签
  s=re_comment.sub('',s)#去掉HTML注释
  #去掉多余的空行
  blank_line=re.compile('\n+')
  s=blank_line.sub('\n',s)
  return s
