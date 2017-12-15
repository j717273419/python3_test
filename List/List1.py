list = ["a","b",3]
for item in list:
    print(item,end=" ")
# print 函数的 end 关键参数来表示以空格结束输出，而不是通常的换行。

# python直接获取集合中的指定信息，组合成一个新的List
list2 = [item for item in list]
print(list2)

list2.append(3)
print(list2)


list3 = [item for item in list2 if item != 3]
print(list3)