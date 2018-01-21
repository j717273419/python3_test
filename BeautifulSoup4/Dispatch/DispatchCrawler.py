# coding = "utf8"

__author__ = "wdj"
__date__ = "2017-12-27"
__version__ = "0.1"

'''
功能：调度2个Web Crawler每天执行抓取任务
'''

from apscheduler.schedulers.blocking import BlockingScheduler
from BeautifulSoup4.CnBeta.Cnbeta2Mysql import CrawCnbeta
from BeautifulSoup4.Solidot.Solidot2Mysql import CrawSolidot
from datetime import datetime, timedelta
import random


class DispatchHelper:

    # 根据随机数生成时间
    def job_random_time(self):
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        time = "{hour}:{minute}:{second}".format(hour=hour, minute=minute, second=second)
        date = datetime.now() + timedelta(days=1)
        date_string = date.strftime("%Y-%m-%d")
        dt = date_string + " " + time
        return dt

    # 一次性任务，创建后，只会运行一次
    def job_once(self, scheduler, function_name):
        print("execute job : job_once")
        date_time = self.job_random_time()
        print(date_time)
        scheduler.add_job(function_name, 'date', run_date=date_time)
        print(scheduler.print_jobs())


if __name__ == '__main__':
    obj = DispatchHelper()
    cnbeta = CrawCnbeta();
    solidot = CrawSolidot();
    # 定义BlockingScheduler
    blockingScheduler = BlockingScheduler()
    blockingScheduler.add_job(obj.job_once, 'interval', days=1, args=[blockingScheduler, cnbeta.exec_cnbeta])
    blockingScheduler.add_job(obj.job_once, 'interval', days=1, args=[blockingScheduler, solidot.exec_solidot])
    blockingScheduler.start()
