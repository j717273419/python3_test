# _*_ coding: utf-8 _*_

# 要先通过pip安装python连接mysql的库，pip install PyMysql
import pymysql

conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='news')

cur = conn.cursor()
sql_text = "Insert Into news_cnbeta(id,news_title,news_content) values()"
cur.execute("Insert Into ")

print(cur.description)
print()

for row in cur:
    print(row)

cur.close()
conn.close()
