# coding=utf8
# create time : 2017-04-22
__author__ = "wdj"

# 功能：抓取CnBeta网站的标题和链接，并保存到数据库中
# 加入去重功能，如果标题和链接一样，就不再写入
import sys
sys.path.append("..")
import Common.DbHelperMysql.DbHelper


