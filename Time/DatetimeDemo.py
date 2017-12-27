from datetime import datetime,timedelta
import random


print(datetime.now())
# python3日期加减使用timedelta
print(datetime.now() + timedelta(days=1))


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

for i in range(1,20):
    print(job_random_time())