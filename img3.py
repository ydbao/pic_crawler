# -*- coding: utf-8 -*-
# 花瓣网

import re
import os
import requests
from time import sleep, time
from random import choice
from multiprocessing.dummy import Pool as ThreadPool

# 图片存储地址
down_dir = '/Users/renjialiang/Desktop/huaban/'

page_count = 0
photo_number = 0
down_data = []

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
TimeOut = 30


def downfile(down_data):
    print u"开始下载：", down_data[0], down_data[1]
    try:
        resource = requests.get(down_data[1], stream=True, headers=head).content
        with open(down_data[0], 'wb') as file:
            file.write(resource)
    except Exception as e:
        print "下载失败" + str(e)


def request_page_text(url):
    try:
        Page = requests.session().get(url, headers=head, timeout=TimeOut)
        Page.encoding = 'utf-8'
        return Page.text
    except Exception as e:
        print "请求失败了...重试中(5s)" + str(e)
        sleep(5)
        print "暂停结束"
        request_page_text(url)


def request_url_download():
    # print(url)
    global page_count
    page_count += 1
    global photo_number
    print page_count
    text = request_page_text(url_query+str(page_count))
    pattern = re.compile('{"pin_id":(\d*?),.*?"key":"(.*?)",.*?"like_count":(\d*?),.*?"repin_count":(\d*?),.*?}', re.S)
    # 参数re.S 是正则表达式，编译参数标识re.DOTALL，即.匹配除、\n 所有字符

    img_query_items = re.findall(pattern, text)
    for url_items in img_query_items:
        photo_number += 1
        max_pin_id = url_items[0]
        x_key = url_items[1]
        print "开始下载第{0}张图片".format(photo_number)
        url_item = url_image + x_key
        filename = down_dir + str(max_pin_id) + ".jpg"
        if os.path.isfile(filename):
            print "文件存在：" + filename
            continue
        down_data.append([filename, url_item])
        if photo_number >= image_numbers:
            return down_data
    if len(img_query_items) != 0:
        request_url_download()
    return down_data


if __name__ == '__main__':
    start_time = time()
    url_image = 'http://hbimg.b0.upaiyun.com/'
    query_string = raw_input('请输入要查询的关键词：')
    global image_numbers
    image_numbers = int(input('下载多少张：'))
    url_query = "http://huaban.com/search/?q=" + query_string + "&per_page=30&wfl=1&page="
    if not os.path.exists(down_dir):
        os.makedirs(down_dir)
        os.chdir(down_dir)
    else:
        os.chdir(down_dir)
    s = request_url_download()
    pool = ThreadPool(1)
    list(pool.map(downfile, s))
    pool.close()
    pool.join()
    end_time = time()
    print '共下载%s张素材，耗时%.2fs' % (len(s), end_time - start_time)