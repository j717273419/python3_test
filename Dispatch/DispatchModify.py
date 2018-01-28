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
    sched.print_jobs()

def modify():
    #重新规划job
    sched.reschedule_job('test_job1', trigger='interval', seconds=6)
    sched.print_jobs()

# 定义BlockingScheduler
sched = BlockingScheduler()
sched.add_job(job, 'interval', seconds=3, id='test_job1')
sched.add_job(job, 'interval', seconds=5, id='test_job2')
sched.add_job(modify, 'interval', seconds=10, id='test_job3')
sched.start()
print('hi')
# sched.modify_job('test_job1', seconds=6)