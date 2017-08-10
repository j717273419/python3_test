#coding:utf-8
set1 = set(["1","2","3"])
print(set1)

set2 = set([4,5,6])
print(set2)

print(set1 & set2)

set3 = set([5,6,7])

#交集
set4 = set2 & set3
print(set4)
#并集
set5 = set2 | set3
print(set5)
#差集，注意方向，在先和在后的结果不一样的
set6 = set2 - set3
print(set6)

set7 = set3 - set2
print(set7)

#遍历set
set8 = set([1,3,4,8])
for i in set8:
    print(i)


