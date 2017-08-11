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
    #anchors = html_soup.select('result c-container ')
    result = html_soup.select('#1')
    print(result)
    title = html_soup.select('html head title')
    # select返回的结果是一个list，所以获取结果要遍历
    print(type(title))
    print(title[0].string)
   # for i in range(len(anchors)):
    #    print(anchors[i].attrs['title'])
     #   print(anchors[i].attrs['href'])


def main():
    url = "https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd=%E6%96%B0%E9%97%BB&oq=%25E5%25B9%25BF%25E5%25B7%259E%25E5%25A4%25A9%25E6%25B0%2594&rsv_pq=efdc98c600042e6f&rsv_t=df36QUkmn3Q2lMmPx7Ijwq1TdMTVAdJhduU9P8l%2Bryzj7O0aXvgYFR0Pe6Y&rqlang=cn&rsv_enter=1&rsv_sug3=5&rsv_sug1=4&rsv_sug7=100&rsv_sug2=0&inputT=847&rsv_sug4=3094"
    html_doc = get(url)
    detect(html_doc)


if __name__ == "__main__":
    main()