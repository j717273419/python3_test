#create time: 2017-04-22
#encoding=utf-8
from urllib import request
from urllib import parse
from bs4 import BeautifulSoup

DEFAULT_HEADERS = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0"}
DEFAULT_TIMEOUT = 130


def get(url):
    req = request.Request(url, headers=DEFAULT_HEADERS)
    response = request.urlopen(req, timeout=DEFAULT_TIMEOUT)
    content = ""
    if response:
        content = response.read().decode("utf8")
        response.close()
    return content


def detect(html_doc):
    html_soup = BeautifulSoup(html_doc, "html.parser")

    #获取标题的Tag
    print("title:",html_soup.title.name)
    #获取标题的具体文本
    print("title:",html_soup.title.string)

    print("body:",html_soup.body.name)
    print("title:",(html_soup.body.findAll("div",{"class","title"})))
    print("time:",(html_soup.body.findAll("div",{"class","time"})))
    print("content:",(html_soup.body.findAll("div",{"class","content"})))
    content = html_soup.body.findAll("div",{"class","content"})
    if(len(content) > 0):
        print("News Content:",content[0].p)


def main():
    url = "http://m.cnbeta.com/wap/view/650325.htm"
    html_doc = get(url)
    detect(html_doc)


if __name__ == "__main__":
    main()