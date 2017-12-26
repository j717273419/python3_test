# coding = 'uft8'
# create-time = '2017-12-26'
__author__ = "wdj"
__version__ = "0.1"

'''
周一到周五每天早上6点半喊我起床的例子
'''

from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

# 输出时间
def job():
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
# BlockingScheduler
scheduler = BlockingScheduler()
scheduler.add_job(job,"cron",day_of_week="1-5",hour=6,minute=30)
scheduler.start()