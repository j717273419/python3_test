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
t1 = threading.Thread(target=music,args=("少年十五二十时",))
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
# 设置了子线程daemon=True才会在主线程结束的时候强制终止。。
# 线程有一个布尔属性叫做daemon。表示线程是否是守护线程，默认取否。
#
# 当程序中的线程全部是守护线程时，程序才会退出。只要还存在一个非守护线程，程序就不会退出。
#
# 主线程是非守护线程。
#
# 所以如果子线程的daemon属性不是True，那么即使主线程结束了，子线程仍然会继续执行。不存在你担心的问题。只有子线程的daemon属性是True时才存在你说的问题。