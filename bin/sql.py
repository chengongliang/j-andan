#!/usr/bin/env python
#coding:utf8
#author:chengongliang
import sys
import MySQLdb

class mySQL():

    def __init__(self):
        try:
            self.conn = MySQLdb.connect(host='localhost',user='root',passwd='',db='jandan',port=3306)
            self.cur = self.conn.cursor()
        except MySQLdb.Error,e:
            print "MySQL error %d:%s" % (e.args[0],e.args[1])
            sys.exit(1)

    def get_agent(self):
        #获取agent列表
        self.cur.execute("select info from configs where config='agent'")
        sql_data = self.cur.fetchall()
        List = sql_data[0][0].split("','")
        return List

    def get_num(self):
        #获取上次爬取的页码
        self.cur.execute("select info from configs where config='page_num'")
        num = self.cur.fetchall()[0][0]
        return num

    def put_num(self,conf,num):
        #写入新页码
        self.cur.execute("UPDATE `jandan`.`configs` SET `info`=%s WHERE (`config`=%s)",[num, conf])
        self.conn.commit()

    def put_ooxx(self,num,url,oo,xx):
        #写入图片相关信息
        self.cur.execute("INSERT INTO `jandan`.`ooxx` (`page_num`, `url`, `oo`, `xx`) SELECT %s, %s, %s, %s FROM dual WHERE NOT EXISTS (SELECT url FROM ooxx WHERE url = %s)",[num,url,oo,xx,url])
        self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()
