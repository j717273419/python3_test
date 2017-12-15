# coding = utf8
# create_time = 2017-12-14
__author__ = "wdj"

from urllib import request
from bs4 import BeautifulSoup

class ParseSolidot:
    DEFAULT_HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"}
    DEFAULT_TIMEOUT = 15
    HOST = "http://www.solidot.org"


    def get(self,url):
        req = request.Request(url, headers=self.DEFAULT_HEADERS)
        response = request.urlopen(req, timeout=self.DEFAULT_TIMEOUT)
        if response:
            content = response.read().decode("utf8")
            response.close()
        return content


    def detect(self,html_doc):
        html_soup = BeautifulSoup(html_doc, "html.parser")
        # 抓取正文
        div_list = html_soup.body.findAll("div", {"class", "bg_htit"})
        return_list = []
        for row in div_list:
            return_tuple = (row.find_all("a")[-1].string,self.HOST + row.find_all("a")[-1]["href"])
            return_list.append(return_tuple)
        #抓取热门文章
        ul_list = html_soup.body.findAll("li", {"class", "old_blockli"})
        if len(ul_list) > 0:
            a_list = ul_list[0].contents[1].contents
            a_list = [item for item in a_list if item != '\n']
            for row in a_list:
                return_tuple = (row.a.string,self.HOST + row.a["href"])
                return_list.append(return_tuple)
        return return_list

    def main(self):
        url = self.HOST
        html_doc = self.get(url)
        result = self.detect(html_doc)
        return result

if __name__ == "__main__":
    obj = ParseSolidot()
    response = obj.get(obj.HOST)
    result = obj.detect(response)
    for item in result:
        print(item)
