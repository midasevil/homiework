# -*- coding: utf-8 -*-
from datetime import datetime
import pymysql
from scrapy_redis.pipelines import RedisPipeline
import urllib

class AmojPipeline(object):

    """"  add field datetime and spider.name to item"""
    def process_item(self, item, spider):
        item["crawled"] = datetime.now()
        item["spider"] = spider.name
        return item


class MySQLPipeline(object):

    """    Synchronization IO， just for convenience, should not be used    """
    def __init__(self):
        self.conn= pymysql.connect(
            host='localhost',
            user='root',
            passwd='lsrandcj340504',
            charset='utf8mb4',
            use_unicode=False,
            db='amoj'
        )
        self.cursor = self.conn.cursor( )

    def process_item(self, item, spider):
        print('start')
        conn = self.conn
        sql = 'insert into amoz(pid,title,papercover,hardcover,kindle,comments,crawled,spider,morechoices) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        cursor = self.cursor
        try:
            cursor.execute(sql, (item["pid"], item["title"],item['papercover'],item['hardcover'],item['kindle'],\
                                 item['comments'],item['crawled'],item['spider'],item['morechoices']))
            conn.commit()
            print('insert succeed')
        except Exception as e:
            print(e)

        return item

class StartRequestPipeline(RedisPipeline):

    """export url that take title as keyword into redis as requests_urls for other spiders"""
    def _process_item(self, item, spider):
        key = self.item_key(item, spider)
        keyword = item['title']
        keyword = urllib.parse.quote(keyword)
        url = 'https://search.jd.com/bookadvsearch?keyword={keyword}&author=&publisher=&isbn=&discount=&ep1=&ep2=&ap1=&ap2=&pty1=&ptm1=&pty2=&ptm2=&enc=utf-8'.format(keyword=keyword)
        self.server.lpush(key, url)
        return item

    def item_key(self, item, spider):
        return self.key

