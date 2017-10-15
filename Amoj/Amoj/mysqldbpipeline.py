#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from twisted.enterprise import adbapi
import pymysql
import pymysql.cursors
import logging

logger = logging.getLogger(__name__)


class MySQLPipeline(object):
    """"this pipeline export item  into MySQL"""

    def __init__(self,dbpool):
        self.dbpool=dbpool
    @classmethod
    def from_settings(cls,settings):
        dbparams = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool('pymysql', **dbparams)
        return cls(dbpool)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        query.addErrback(self._handle_error, item, spider)
        return item

    def _conditional_insert(self, tx, item):
        sql = 'insert into amoj(pid,title,papercover,hardcover,kindle,comments,crawled,spider,morechoices) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        params = (item["pid"], item["title"], item['papercover'], item['hardcover'], item['kindle'], item['comments'], item['crawled'], item['spider'], item['morechoices'])
        tx.execute(sql, params)

    def _handle_error(self, failure, item, spider):
        logger.error('***********************database operation exception!!***************************')
        logger.error(failure)
