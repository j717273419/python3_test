#coding=gbk

states = {}
print type(states)

dict01 = {"Name":"xxx","Age":"12"}
print dict01

print dict01.keys()

print dict01.values()

print dict01.get("Name")

print dict01.get("Age")

dict01["Age"] = 22
print dict01['Age']

dict01.pop("Age")

print dict01

print dict01.has_key("Name")
print dict01.has_key("Age")
# in
print "Name" in dict01

'''
compare
'''
dict02 = {1:20,2:40}
dict03 = {10:200,20:400}
dict04 = {20:400,10:200}
print dict02,dict03


var = dict02 == dict03

print var

print dict03 == dict04


# 字典排序

# sort by key
dictSort = {"a":20,"c":30,"d":2,"b":3000}
dictSort=sorted(dictSort.items(),key=lambda d:d[0])
print dictSort

#sort by value default sort by ascending
dictSort = {"a":20,"c":30,"d":2,"b":3000}
dictSort = sorted(dictSort.items(),key=lambda d:d[1])
print dictSort

#sort by value descending
dictSort = {"a":20,"c":30,"d":2,"b":3000}
dictSort = sorted(dictSort.items(),key=lambda d:d[1],reverse=True)
print dictSort
print type(dictSort)

#foreach
print "foreach dict"
dictFor = {"a":20,"c":30,"d":2,"b":3000}
for(x,y) in dictFor.items():
    print "key:"+x+",value:"+str(y)

for x,y in dictFor.items():
    print "key:"+x+"value:"+str(y)