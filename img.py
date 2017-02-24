# -*- encoding: utf-8 -*-
# 图虫网g

import urllib2
import re
from urllib import urlopen
import uuid
from time import time


# 图片存储地址
down_dir = '/Users/renjialiang/Desktop/huaban/'

# 获取二级页面url
def findUrl2(html):
    re1 = r'https://tuchong.com/\d+/\d+/|http://\w+(?<!photos).tuchong.com/\d+/'
    url2list = re.findall(re1, html)
    url2lstfltr = list(set(url2list))
    url2lstfltr.sort(key=url2list.index)
    return url2lstfltr


# 获取html文本
def getHtml(url):
    try:
        html = urllib2.urlopen(url).read().decode('utf-8')  # 解码为utf-8
        return html
    except Exception, e:
        print e
        return ''


if __name__ == '__main__':
    query_string = raw_input('请输入要查询的关键词：')
    pageNo = int(input('从第一页下载到多少页：'))
    start_time = time()
    i = 1
    count=0
    while i <= int(pageNo):
        if i == 1:
            html = getHtml("https://tuchong.com/tags/"+query_string+"/?type=new")
        else:
            html = getHtml("https://tuchong.com/tags/"+query_string+"/?type=new&page=" + str(i))
        i += 1
        if html != '':
            detllst = findUrl2(html)
            for detail in detllst:
                html2 = getHtml(detail)
                re2 = r'https://photo.tuchong.com/\d+/f/\d+\.jpg'
                imglist = re.findall(re2, html2)
                for l in imglist:
                    count += 1
                    img_net = urlopen(l).read()  # 打开网络图片
                    img_name = down_dir + str(uuid.uuid1()) + '.jpg'
                    img_local = open(img_name, 'wb')  # 打开本地文件
                    print '正在下载第 ' + str(count) + ' 张'
                    img_local.write(img_net)  # 将网络文件写入到本地
                    img_local.close()  # 关闭本地文件
        else:
            break

    end_time = time()
    print('共下载%s张素材，耗时%.2fs' % (count, end_time - start_time))