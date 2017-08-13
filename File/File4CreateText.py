import os

#获取当前路径
print("当前路径是：",os.getcwd())

#获取键盘录入的数据
input_value = input("raw_input:")
print("你输入的值是：",input_value)

#python3创建文件
cwd = os.getcwd()
file_name = cwd + "\\{0}.txt".format(input_value)
f = open(file_name,"wt")
for a in range(0,10):
    f.write(str(a))
f.close()


#python3创建文件,写入的内容换行
cwd = os.getcwd()
file_name = cwd + "\\test2.txt"
f = open(file_name,"wt")
for a in range(30,100):
    f.write(str(a)+"\n")
f.close()


