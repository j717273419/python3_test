#coding=utf-8
a=10
print("输出a的值是",(a))

print("输出a的值是%d" % a)

b=90

print("a的值是%d,b的值是%d" % (a,b))

print("a的值是%d,b的值是%d，a+b=%d" % (a,b,a+b))

#python3中字符串使用占位符0,1和大括号
print(("{0},{1},{0}").format("haha","me"))


#python3中字符串使用占位符别名和大括号
print(("{a},{b},{a}").format(a="hahaaaa",b="mebbbb"))


