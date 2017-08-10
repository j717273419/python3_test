import re

p = re.compile(r"\d+")
str = "abc123efg456"
result = re.findall(p,str)
print(result)
print(type(result))

relink = '<a href="(.*)">(.*)</a>'
info = '<a href="http://www.baidu.com">baidu</a>'
cinfo = re.findall(relink,info)
print(cinfo)
print(type(cinfo))