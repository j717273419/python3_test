import os

print(os.path)

print(os.getcwd())

print(os.path.isfile("inline.txt"))

print(os.path.exists("dd"))

# python3 创建目录
if not os.path.exists('dd'):
    os.mkdir('dd')
print('dd has been created')
print(os.path.exists("dd"))

# python3 创建文件
print('python3 创建文件:')

print(os.path.isfile("inline.txt"))
print(os.path.exists("inline.txt"))

fileName = "aa/a.txt"
if not os.path.exists(fileName):
    print('not exists {fileName}'.format(fileName=fileName))
    if not os.path.exists('aa'):
        os.mkdir('aa')
    f = open(fileName, 'w')
    f.close()
    print("file has created")
