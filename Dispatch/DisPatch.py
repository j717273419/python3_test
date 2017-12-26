# coding = 'uft8'
# create-time = '2017-12-26'
__author__ = "wdj"
__version__ = "0.1"
'''
Python任务调度，使用APSchduler库来实现
下面是一个简单使用BlockingScheduler，并使用默认内存存储和默认执行器。
(默认选项分别是MemoryJobStore和ThreadPoolExecutor，其中线程池的最大线程数为10)。
配置完成后使用start()方法来启动。
参考链接：http://debugo.com/apscheduler/
'''
from apscheduler.schedulers.blocking import BlockingScheduler

def my_job():
    print('hello world')
sched = BlockingScheduler()
sched.add_job(my_job, 'interval', seconds=5)
sched.start()
