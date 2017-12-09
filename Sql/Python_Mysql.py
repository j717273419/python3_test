# _*_ coding: utf-8 _*_

# 要先通过pip安装python连接mysql的库，pip install PyMysql
import pymysql

conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='mysql')

cur = conn.cursor()
cur.execute("SELECT * FROM user ")

print(cur.rowcount)
print()

for row in cur:
    print(row)

cur.close()
conn.close()
