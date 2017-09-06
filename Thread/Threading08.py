#coding=utf-8
from time import sleep, ctime
import threading

def super_player(file,time):
    for i in range(2):
        print('Start playing： %s! %s' %(file,ctime()))
        sleep(time)

#播放的文件与播放时长
list = {'爱情买卖.mp3':1,'阿凡达.mp4':1.2,'我和你.mp3':1.1}

threads = []
files = range(len(list))

#创建线程
for file,time in list.items():
    t = threading.Thread(target=super_player,args=(file,time))
    threads.append(t)

if __name__ == '__main__':
    #启动线程
    for i in files:
        threads[i].start()
    #阻塞主线程，等待子线程全部执行完成后，才执行主线程
    for i in files:
        threads[i].join()

    #主线程
    print('end:%s' %ctime())