#!/usr/bin/python
#encoding:utf8
#author:chengongliang

import re
import os
import sys
import random
import requests
from sql import mySQL

s = mySQL()

def getHtml(url):
    #获取html
    #n = 0
    flag = True
    agents = s.get_agent()
    while flag:
        headers = {'User-Agent':random.choice(agents)}
        request = requests.get(url, headers=headers)
        if request.ok:
            html = request.content
            flag = False
            return html
        else:
            print "Bad agent: %s" % headers['User-Agent']
    #while n < len(agent):
    #    headers = {'User-Agent':agent[n]}
    #    request = requests.get(url, headers=headers)
    #    if request.ok:
    #        html = request.content
    #        return html
    #        break
    #    else:
    #        n += 1
    print "连接服务器失败，错误码：%s" % request.status_code
    sys.exit(1)


def getUrl_list(html,p):
    #获取图片链接
    re_img = re.compile(r'<div class="text">.*?<p>.*?<a href="(http://ww.*?)".*?<div class="vote".*?<span id="cos_support.*?">(\d+)</span>.*?<span id="cos_unsupport.*?">(\d+)</span>', re.S)
    url_list = []
    items = re_img.findall(html)
    for url,oo,xx in items:
        try:
            if int(oo)/int(xx) >= 10:
                s.put_ooxx(p,url,oo,xx)
                url_list.append(url)
            elif int(oo) >= 200 and int(xx) <= 30:
                s.put_ooxx(p,url,oo,xx)
                url_list.append(url)
        except ZeroDivisionError,e:
            s.put_ooxx(p,url,oo,xx)
    return url_list

def getCurrent():
    #获取最新页码
    start_page = getHtml("http://jandan.net/ooxx")
    current = re.compile(r'<div class="comments">.*?<span class="current-comment-page">\[(\d+)\]</span>',re.S)
    try:
        page = current.findall(start_page)[0]
        print page
        s.put_num('page_num',page)
        return page
    except IndexError ,e:
        print "Error agent!"
        sys.exit(1)

def save_img(url,name):
    #保存图片
    if not os.path.exists('src/%s' %name):
        with open('src/%s' %name, 'wb') as fd:
            img = getHtml(url)
            fd.write(img)

def download(url_list):
    #切分链接，获取图片名
    for url in url_list:
        name = url.split('/')[-1]
        save_img(url,name)

def main():
    last_num = s.get_num()
    current_num = getCurrent()
    list_pages = range(int(last_num),int(current_num)+1)
    print list_pages
    for p in list_pages:
        url = 'http://jandan.net/ooxx/page-%s#comments' % p
        print "~~正在下载第%s页~~" % p
        html = getHtml(url)
        url_list = getUrl_list(html,p)
        download(url_list)
    s.close()
