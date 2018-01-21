import logging
import os
from datetime import datetime

'''
根据日期生成日志文件，每天生成一个日志文件
'''

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

yearMonthStr = datetime.now().strftime("%Y-%m")
if not os.path.exists(yearMonthStr):
    os.mkdir(yearMonthStr)
dateStr = datetime.now().strftime("%Y-%m-%d")
pathStr = "{yearMonth}/test-{date}.log".format(date=dateStr, yearMonth=yearMonthStr)
handler = logging.FileHandler(pathStr)
handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s ')
handler.setFormatter(formatter)

logger.addHandler(handler)

logger.info("Hello logging")