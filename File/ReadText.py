import os;

#python3读取文本内容
cwd = os.getcwd()
filename = "\inline.txt"
path = cwd + filename
read_model = "r"
f = open(path,read_model)
print(f.read())
f.close()


#python3读取文本内容
#1,如果直接写文件名，不加路径python会读取当前脚本所在目录的文件
#2，read()方法直接返回文本中的所有内容。
cwd = os.getcwd()
filename = "test2.txt"
path = filename
read_model = "r"
f = open(path,read_model)
print(f.read())
f.close()


#python3读取文本内容
#读取指定行数的内容
cwd = os.getcwd()
filename = "test2.txt"
path = filename
read_model = "r"
print("读取指定行数的内容")
f = open(path,read_model)
print(f.readline())

print("返回每一行的内容")
f = open(path,read_model)
print(f.readlines())
print(type(f.readlines()))
f.close()


