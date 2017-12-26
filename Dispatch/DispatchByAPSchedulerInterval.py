# coding = "utf8"
__author__ = "wdj"
__version__ = "0.1"
__date__ = "2017-12-26"

'''
每隔3秒输出一次当前时间
'''

from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

def job():
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
# 定义BlockingScheduler
sched = BlockingScheduler()
sched.add_job(job, 'interval', seconds=3)
sched.start()