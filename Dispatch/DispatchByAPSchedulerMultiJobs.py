# coding = "utf8"
__author__ = "wdj"
__version__ = "0.1"
__date__ = "2017-12-26"

'''
每隔3秒输出一次当前时间
'''

from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime


def job1():
    print("job1:" + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

def job2():
    print("job2:" + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


def job3():
    print("job3:" + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


# 定义BlockingScheduler
sched = BlockingScheduler()
sched.add_job(job1, 'interval', seconds=2)
sched.add_job(job2, 'interval', seconds=2)
sched.add_job(job3, 'interval', seconds=2)
sched.start()