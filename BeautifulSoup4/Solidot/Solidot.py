# coding = "utf8"
# create_time = 2017-12-14
__author__ = "wdj"

class Solidot:
    # 功能：抓取Solidot网站的标题和链接，并保存到数据库中
    # 加入去重功能，如果标题和链接一样，就不再写入
    import ParseSolidot
    from BeautifulSoup4.Common.DbHelperMysql.DbHelper import DbHelper
    solidot = ParseSolidot.ParseSolidot()
    content = solidot.main()
    DbHelper().batch_insert(content)