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


def post(url, **paras):
    param = parse.urlencode(paras).encode("utf8")
    req = request.Request(url, param, headers=DEFAULT_HEADERS)
    response = request.urlopen(req, timeout=DEFAULT_TIMEOUT)
    content = ""
    if response:
        content = response.read().decode("utf8")
        response.close()
    return content


def detect(html_doc):
    html_soup = BeautifulSoup(html_doc, "html.parser")
    anchors = html_soup.select('a[href^="magnet:?xt"]')
    for i in range(len(anchors)):
        print(anchors[i].attrs['title'])
        print(anchors[i].attrs['href'])


def main():
    url = "https://www.torrentkitty.tv/search/"
    html_doc = post(url, q=parse.quote("超人"))
    detect(html_doc)


if __name__ == "__main__":
    main()