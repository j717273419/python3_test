import time
import random

print(random.random())

print(random.uniform(10,20))

print(random.randint(10,11))
i=0;

sec = random.randint(3,10)
while(i < 10):
    i = i+1
    time.sleep(sec)
    print(i)