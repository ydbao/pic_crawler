# -*- coding: utf-8 -*-
# 百度图片

import requests
import re
from random import choice
import uuid


MaxSearchPage = 1
CurrentPage = 0
save_path = "/Users/renjialiang/Desktop/huaban/" # 默认储存位置

UserAgent = [
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.2)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
    'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12',
    'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0',
    'Opera/8.0 (Macintosh; PPC Mac OS X; U; en)',
    'Opera/9.27 (Windows NT 5.2; U; zh-cn)',
    'Mozilla/5.0 (Windows; U; Windows NT 5.2) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6',
    'Mozilla/5.0 (iPhone; U; CPU like Mac OS X) AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/4A93 Safari/419.3',
    'Mozilla/5.0 (Windows; U; Windows NT 5.2) AppleWebKit/525.13 (KHTML, like Gecko) Version/3.1 Safari/525.13'
]

user_agent = choice(UserAgent)
head = {'User-Agent': user_agent}

def imageFiler(content):  # 通过正则获取当前页面的图片地址数组
    return re.findall('"objURL":"(.*?)"', content, re.S)


def nextSource(content):  # 通过正则获取下一页的网址
    next = re.findall('<div id="page">.*<a href="(.*?)" class="n">', content, re.S)[0]
    print("---------" + "http://image.baidu.com" + next)
    return next


def spidler(source):
        content = requests.get(source).text  # 通过链接获取内容
        imageArr = imageFiler(content)  # 获取图片数组
        global CurrentPage
        CurrentPage += 1
        print("Current page:" + str(CurrentPage) + "**********************************")
        for imageUrl in imageArr:
            print(imageUrl)
            filename = save_path + str(uuid.uuid1()) + '.jpg'
            try:
                req = requests.get(imageUrl, headers=head, stream=True)
                if req.status_code != 404:
                    with open(filename, 'wb') as file:
                        file.write(req.content)
            except Exception as e:
                print "下载失败" + str(e)
        else:
            if CurrentPage < MaxSearchPage:
                if nextSource(content):
                    spidler("http://image.baidu.com" + nextSource(content))  # 爬取完毕后通过下一页地址继续爬取


def beginSearch(key, page):
    global MaxSearchPage
    MaxSearchPage = page
    source = "http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=" + str(key) + "&ct=201326592&v=flip"
    spidler(source)


if __name__ == '__main__':
    query_string = raw_input('请输入要查询的关键词：')
    pageNo = int(input('从第一页下载到多少页：'))
    beginSearch(query_string, pageNo)
