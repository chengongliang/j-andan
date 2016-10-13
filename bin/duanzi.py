#!/usr/bin/env python
#coding:utf8
#author:chengongliang

import re
from ooxx import s,getHtml,getCurrent

def parse():
    data = getHtml('http://jandan.net/duan')
    re_content = re.compile(r'<div class="text">.*?<p>(.*?)</p>',re.S)
    content = re_content.findall(data)
    replaceBR = re.compile(r'<br />')
    new_content = []
    for i in content:
        i = replaceBR.sub('\n',i)
        new_content.append(i)
    return new_content

if __name__ == '__main__':
    num_info = 'duan_page_num'
    start_page = 'http://jandan.net/duan'
    last_num = s.get_num(num_info)
    current_num = getCurrent(start_page,num_info)
    print last_num,current_num
    content = parse()
    for c in content:
        print '%s \n' % c.decode("utf8")
