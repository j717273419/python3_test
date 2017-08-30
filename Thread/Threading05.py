import threading
from time import ctime,sleep

def music(func):
    for i in range(2):
        print("I was listening to music",func,i,ctime())
        sleep(1)

def movie(func):
    for i in range(2):
        print("I was at the movie !",func,i,ctime())
        sleep(5)

threads = []
t1 = threading.Thread(target=music,args=("少年二十五六时",))
threads.append(t1)
t2 = threading.Thread(target=movie,args=("The Shawshank Redemption",))
threads.append(t2)

if __name__ == '__main__':
    for i in threads:
        i.setDaemon(True)
        i.start()
    i.join()

    print("all over",ctime())

#子线程（muisc 、movie ）和主线程（print "all over %s" %ctime()）都是同一时间启动，
# 但由于主线程执行完结束，所以导致子线程也终止。
