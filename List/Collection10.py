bri = set(["brazil","russia","india"])
print("india" in bri)

bri.add("china")
print(bri)

#set 获取值的方式比较特殊，不能使用索引取值
#但是可以这样
l = list(bri)[3]
print(l)
