# coding = "utf8"
# create_time = 2017-12-14
__author__ = "wdj"

from BeautifulSoup4.Solidot.Solidot import SolidotParse
from BeautifulSoup4.Common.DbHelperMysql.DbHelper import DbHelper


class CrawSolidot:
    # 功能：抓取Solidot网站的标题和链接，并保存到数据库中
    # 加入去重功能，如果标题和链接一样，就不再写入


    def exec_solidot(self):
        print("exec_solidot CrawSolidot")
        solidot = SolidotParse()
        content = solidot.exec_solidot()
        DbHelper().batch_insert(content)


if __name__ == "__main__":
    print("__main__ CrawSolidot")
    solidot = SolidotParse()
    content = solidot.main()
    DbHelper().batch_insert(content)
