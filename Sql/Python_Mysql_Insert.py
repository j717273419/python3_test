# _*_ coding: utf-8 _*_

# 要先通过pip安装python连接mysql的库，pip install PyMysql
import pymysql

# 解决python使用pymysql往mysql数据库插入中文时报错的问题
# 在连接时，指明编码参数charset='utf8'
conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='news',charset='utf8')

cur = conn.cursor()
sql_text = "Insert Into news_cnbeta(news_title,news_content) values('{title}','{content}')".format(title="小米6",content="雷军又在玩饥饿营销啦")
cur.execute(sql_text)
conn.commit()

cur.close()
conn.close()
