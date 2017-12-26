# coding = "utf8"
__author__ = "wdj"
__date__ = "2017-12-26"
__version__ = "0.1"

'''
功能：实现在一周内随机的某些天，随机一个时间来执行任务
思路1：设置一个数值区间，随机取一个值。eg.[1-7],
然后根据apscheduler的一次性任务和循环任务，利用循环任务创建一次性任务，
来实现随机时间启动任务
思路2：设置一个循环任务，然后在每次使用之后，通过修改job来实现随机任务Random Job
'''

from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
