#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from lxml import etree
from jinS.items import JinsItem
import re
import urllib

def safeget(l, index, default=None):
    try:
        return l[index]
    except (IndexError, TypeError):
        return default

class MySpider(RedisSpider):
    name = 'jins'
    p = re.compile(r'keyword=(.*?)&author')


    def parse(self, response):
        item = JinsItem()

        url = response.request.url
        p = self.p
        title = p.findall(url)[0]
        title = urllib.parse.unquote(title)

        html = etree.HTML(response.text)
        l = html.xpath('//li[@data-sku]')
        if not safeget(l,0):
            return None
        for li in l:
            jtitle = li.xpath('.//a[@onclick]/em//text()')
            if len(jtitle) == 0:
                item['jtitle'] = None

            item['jtitle'] = ''.join(jtitle)
            jprice = li.xpath('.//strong//i/text()')
            item['jprice'] = safeget(jprice,0)
            jcomments = li.xpath('.//strong/a[@onclick]/text()')
            item['jcomments'] = safeget(jcomments,0)
            shop = li.xpath('.//a[@class="curr-shop"]/text()')
            if shop == []:
                item['jshop'] = ['京东自营']
            else:
                item['jshop'] = safeget(shop, 0)
            item['title'] = title
            pid = li.xpath('.//div[@class="p-name"]/a/@href')[0]
            p = re.compile('item.jd.com/(\d+?).html')
            item['jpid'] = p.findall(pid)[0]

            yield item









