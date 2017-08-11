#!/usr/bin/env python
# coding:utf8
# author:chengongliang

import re
import hashlib
from wechat import WE
from ooxx import s, getHtml, getCurrent

w = WE()


def parse(url):
    data = getHtml(url)
    re_content = re.compile(
        r'<div class="text">.*?<p>(.*?)</p>.*?<div class="jandan-vote".*?<span class="tucao-like-container">.*?\[<span>(\d+)</span>].*?<span class="tucao-unlike-container">.*?\[<span>(\d+)</span>\]', re.S)
    items = re_content.findall(data)
    replaceBR = re.compile(r'<br />')
    # new_content = []
    dz_list = []
    for c, oo, xx in items:
        try:
            if int(oo) / int(xx) >= 10:
                # c = replaceBR.sub('\n', c).strip()
                c = replaceBR.sub('', c).strip()
                dz_list.append(c)
                md5 = hashlib.md5(c).hexdigest()[:15]
                # print c
                # print md5 + "\n"
                s.put_duan(page_num, c, oo, xx, md5)
        except ZeroDivisionError:
            c = replaceBR.sub('\n', c)
    content = '\n--------- --------- ---------\n'.join(dz_list[1:-1])
    # print content
    w.senddata(content)


if __name__ == '__main__':
    num_info = 'duan_page_num'
    start_page = 'http://jandan.net/duan'
    last_num = int(s.get_num(num_info))
    new_num = last_num + 1
    # current_num = (getCurrent(start_page, num_info))
    # current_num = 1557
    # list_pages = range(int(last_num), int(current_num) + 1)
    list_pages = range(last_num, new_num)
    s.put_num(num_info, new_num)
    print list_pages
    for page_num in list_pages:
        url = 'http://jandan.net/duan/page-%s#comments' % page_num
        parse(url)
