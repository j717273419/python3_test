# coding = "utf8"
__author__ = "wdj"
__date__ = "2017-12-26"
__version__ = "0.1"

'''
功能：实现每天在一个随机时间来执行任务
思路1：设置一个数值区间，随机取一个值。eg.[1-7],
然后根据apscheduler的一次性任务和循环任务，利用循环任务创建一次性任务，
来实现随机时间启动任务
思路2：设置一个循环任务，然后在每次使用之后，通过修改job来实现随机任务Random Job
'''

from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime, timedelta
import random


# 输出时间
def job_print(date_time):
    print("execute function : job_print")
    print(date_time)
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


# 根据随机数生成时间
def job_random_time():
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    time = "{hour}:{minute}:{second}".format(hour=hour, minute=minute, second=second)
    date = datetime.now() + timedelta(days=1)
    date_string = date.strftime("%Y-%m-%d")
    dt = date_string + " " + time
    return dt


def job_once(scheduler):
    print("execute job : job_once")
    date_time = job_random_time()
    print(date_time)
    scheduler.add_job(job_print, 'date', run_date=date_time, args=[date_time])
    print(scheduler.print_jobs())


# 定义BlockingScheduler
blockingScheduler = BlockingScheduler()
blockingScheduler.add_job(job_once, 'interval', seconds=2, args=[blockingScheduler])
blockingScheduler.start()
