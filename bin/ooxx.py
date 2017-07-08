#!/usr/bin/python
# _*_ coding:utf8 _*_
# author:chengongliang

import re
import os
import sys
import random
import requests
from sql import mySQL

s = mySQL()


def getHtml(url):
    # 获取html
    # n = 0
    flag = True
    agents = s.get_agent()
    while flag:
        headers = {'User-Agent': random.choice(agents)}
        request = requests.get(url, headers=headers)
        if request.ok:
            # print headers
            html = request.content
            flag = False
            return html
        else:
            print "Bad agent: %s" % headers['User-Agent']
    # while n < len(agent):
    #     headers = {'User-Agent':agent[n]}
    #     request = requests.get(url, headers=headers)
    #     if request.ok:
    #         html = request.content
    #         return html
    #         break
    #     else:
    #         n += 1
    print "连接服务器失败，错误码：%s" % request.status_code
    sys.exit(1)


def getUrl_list(html, p):
    # 获取图片链接
    re_img = re.compile(r'<div class="text">.*?<p><a href="(//w.*?)".*?<span class="tucao-like-container">.*?\[<span>(\d+)</span>].*?<span class="tucao-unlike-container">.*?\[<span>(\d+)</span>\]', re.S)
    url_list = []
    try:
        items = re_img.findall(html)
    except Exception, e:
        items = e
    for url, oo, xx in items:
        try:
            if int(oo) / int(xx) >= 10:
                s.put_ooxx(p, url, oo, xx)
                url_list.append(url)
            elif int(oo) >= 200 and int(xx) <= 30:
                s.put_ooxx(p, url, oo, xx)
                url_list.append(url)
        except ZeroDivisionError:
            s.put_ooxx(p, url, oo, xx)
    return url_list


def getCurrent(url, project):
    # 获取最新页码
    start_page = getHtml(url)
    current = re.compile(r'<div class="comments">.*?<span class="current-comment-page">\[(\d+)\]</span>', re.S)
    try:
        page = current.findall(start_page)[0]
        s.put_num(project, page)
        return page
    except IndexError:
        print "Error agent!"
        sys.exit(1)


def save_img(url, name):
    # 保存图片
    if not os.path.exists('src'):
        os.mkdir('src')
    if not os.path.exists('src/%s' % name):
        with open('src/%s' % name, 'wb') as fd:
            url = 'http:' + url
            img = getHtml(url)
            fd.write(img)


def download(url_list):
    # 切分链接，获取图片名
    for url in url_list:
        name = url.split('/')[-1]
        save_img(url, name)


def main():
    last_num = s.get_num('ooxx_page_num')
    current_num = getCurrent('http://jandan.net/ooxx', 'ooxx_page_num')
    list_pages = range(int(last_num), int(current_num) + 1)
    n = 0
    for p in list_pages:
        url = 'http://jandan.net/ooxx/page-%s#comments' % p
        print "~~正在下载第%s页~~" % p
        html = getHtml(url)
        url_list = getUrl_list(html, p)
        download(url_list)
        n += len(url_list)
    print "~~已下载%s张图片~~" % n
    s.close()
