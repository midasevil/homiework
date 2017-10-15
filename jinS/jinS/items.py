# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JinsItem(scrapy.Item):
    jpid = scrapy.Field()
    jshop = scrapy.Field()
    jtitle = scrapy.Field()
    jcomments = scrapy.Field()
    jprice = scrapy.Field()
    jcrawled =scrapy.Field()
    jspider = scrapy.Field()
    title = scrapy.Field()
