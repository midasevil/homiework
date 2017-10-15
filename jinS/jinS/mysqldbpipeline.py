#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from twisted.enterprise import adbapi
import pymysql
import pymysql.cursors


class MySQLPipeline(object):

    def __init__(self, dbpool):
        self.dbpool = dbpool
    @classmethod
    def from_settings(cls,settings):
        dbparams = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=False,
        )
        dbpool = adbapi.ConnectionPool('pymysql', **dbparams)
        return cls(dbpool)

    def process_item(self,item,spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        query.addErrback(self._handle_error, item, spider)
        return item

    def _conditional_insert(self, tx, item):
        sql = 'insert into jins(jpid,jtitle,title,jcomments,jcrawled,jspider,jprice,jshop) values(%s,%s,%s,%s,%s,%s,%s,%s)'
        params = (item["jpid"], item["jtitle"], item['title'], item['jcomments'], item['jcrawled'], item['jspider'], item['jprice'], item['jshop'])
        tx.execute(sql, params)

    def _handle_error(self, failure, item, spider):
        print('--------------database operation exception!!-----------------')
        print(failure)
