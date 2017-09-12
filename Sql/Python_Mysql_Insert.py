# _*_ coding: utf-8 _*_

# 要先通过pip安装python连接mysql的库，pip install PyMysql
import pymysql

conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='news')

cur = conn.cursor()
sql_text = "Insert Into news_cnbeta(news_title,news_content) values('{title}','{content}')".format(title="apple",content="iphone8")
cur.execute(sql_text)

cur.close()
conn.close()
