#encoding=utf-8
#create time: 2017-12-11
#creator : wdj

from urllib import request
from urllib import parse
from bs4 import BeautifulSoup

class CnBeta:
    DEFAULT_HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"}
    DEFAULT_TIMEOUT = 10
    HOST = "http://m.cnbeta.com"

    def get(self,url):
        req = request.Request(url, headers=self.DEFAULT_HEADERS)
        response = request.urlopen(req, timeout=self.DEFAULT_TIMEOUT)
        content = ""
        if response:
            content = response.read().decode("utf8")
            response.close()
        return content

    def detect(self,html_doc):
        html_soup = BeautifulSoup(html_doc, "html.parser")
        title = html_soup.select('html head title')
        # select返回的结果是一个list，所以获取结果要遍历
        # 获取标题的Tag
        # print("title:", html_soup.title.name)
        # 获取标题的具体文本
        # print("title:", html_soup.title.string)
        # print("body:", html_soup.body.name)
        # print("body:", (html_soup.body.findAll("div", {"class", "list"})))
        title_list = html_soup.body.findAll("div", {"class", "list"})
        return_list = []
        for row in title_list:
            # print("row.title:", row.a.string)
            # print("row.link:", self.HOST + row.a["href"])
            return_tuple = (row.a.string,self.HOST + row.a["href"])
            return_list.append(return_tuple)
        return return_list

    def main(self):
        url = self.HOST + "/wap"
        html_doc = self.get(url)
        result = self.detect(html_doc)
        return result

if __name__ == "__main__":
    obj = CnBeta()
    print(obj.main())









