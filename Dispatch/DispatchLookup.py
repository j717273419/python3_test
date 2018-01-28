# coding = "utf8"
__author__ = "wdj"
__version__ = "0.1"
__date__ = "2017-12-26"

'''
python3使用apscheduler判断是否存在job
'''

from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime


def job():
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    sched.print_jobs()


# 定义BlockingScheduler
sched = BlockingScheduler()
sched.add_job(job, 'interval', seconds=3, id='test_job1')
sched.add_job(job, 'interval', seconds=5, id='test_job2')
print(sched.get_job('test_job1'))
print(sched.get_job('test_job1111'))
print(type(sched.get_job('test_job1111')))
if sched.get_job('test_job1111') is None:
    print("haha")
sched.start()
print('hi')
# sched.modify_job('test_job1', seconds=6)