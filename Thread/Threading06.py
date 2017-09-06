# coding=utf-8
from time import sleep, ctime
import threading


def music(func):
    for i in range(1):
        print('Start playing： %s! %s' % (func, ctime()))
        sleep(2)


def movie(func):
    for i in range(1):
        print('Start playing： %s! %s' % (func, ctime()))
        sleep(5)


def player(name):
    r = name.split('.')[1]
    if r == 'mp3':
        music(name)
    else:
        if r == 'mp4':
            movie(name)
        else:
            print('error: The format is not recognized!')

lists = ['爱情买卖.mp3', '阿凡达.mp4', '金刚.mp4']

threads = []
files = range(len(lists))

# 创建线程
for i in files:
    t = threading.Thread(target=player, args=(lists[i],))
    threads.append(t)

if __name__ == '__main__':
    # 启动线程
    for i in files:
        threads[i].start()

    #for i in files:
        #threads[i].join()



# 主线程
print('end:%s' % ctime())
