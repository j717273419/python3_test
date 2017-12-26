#encoding=utf-8
#create_time: 2017-12-9 9:36:18
#creator: wdj
#function: insert data 2 mysql

import pymysql


class DbHelper:
    # 解决python使用pymysql往mysql数据库插入中文时报错的问题
    # 在连接时，指明编码参数charset='utf8'
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='1234', db='news',charset='utf8')
    cur = conn.cursor()
    # 检测是否已经存在记录
    def articleIsExists(self,news_url) :
        sql_text_check = "select news_title from news_cnbeta where news_url = '{url}'".format(url=news_url)
        #执行sql
        self.cur.execute(sql_text_check)
        self.conn.commit()
        if(self.cur.rowcount > 0):
            return True
        return False

    #插入到数据库
    def insert2mysql(self,news_title,news_url,news_content=""):
        sql_text_insert = "Insert Into news_cnbeta(news_title,news_url,news_content) values('{title}','{url}','{content}')".format(
                        title=news_title,
                        url=news_url,
                        content=news_content)
        #执行sql
        self.cur.execute(sql_text_insert)
        self.conn.commit()

    #插入新闻
    def insert(self,news_title,news_url,news_content=""):
        try:
            if(self.articleIsExists(news_url)):
                return "已经添加过此记录"
            else:
                self.insert2mysql(news_title, news_url,news_content)
                return "添加成功"
        except:
                return "出现异常"


    def batch_insert(self,list):
        try:
            for item in list:
                self.insert(item[0],item[1])

        finally:
            # 关闭sql连接
            self.cur.close()
            self.conn.close()

if __name__ == '__main__':
    obj = DbHelper()
    # result = obj.articleIsExists(news_url='haha')
    result = obj.insert("测试插入", "http://www.jb51.net/article/63833.htm", "content")
    print(result)


