#!/usr/bin/env python
# coding:utf8
# author:chengongliang

import re
import hashlib
from ooxx import s, getHtml, getCurrent


def parse(url):
    data = getHtml(url)
    re_content = re.compile(
        r'<div class="text">.*?<p>(.*?)</p>.*?<div class="vote".*?<span id="cos_support.*?">(\d+)</span>.*?<span id="cos_unsupport.*?">(\d+)</span>', re.S)
    items = re_content.findall(data)
    replaceBR = re.compile(r'<br />')
    # new_content = []
    for c, oo, xx in items:
        try:
            if int(oo) / int(xx) >= 10:
                c = replaceBR.sub('\n', c).strip()
                md5 = hashlib.md5(c).hexdigest()[:15]
                print c
                print md5 + "\n"
                # s.put_duan(page_num,c,oo,xx,md5)
        except ZeroDivisionError:
            c = replaceBR.sub('\n', c)


if __name__ == '__main__':
    num_info = 'duan_page_num'
    start_page = 'http://jandan.net/duan'
    last_num = s.get_num(num_info)
    # current_num = getCurrent(start_page,num_info)
    current_num = 1557
    list_pages = range(int(last_num), int(current_num) + 1)
    print list_pages
    for page_num in list_pages:
        url = 'http://jandan.net/duan/page-%s#comments' % page_num
        parse(url)
