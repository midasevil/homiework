# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AmozItem(scrapy.Item):
    pid = scrapy.Field()
    title = scrapy.Field()
    papercover = scrapy.Field()
    hardcover = scrapy.Field()
    kindle = scrapy.Field()
    comments = scrapy.Field()
    morechoices = scrapy.Field()
    crawled = scrapy.Field()
    spider = scrapy.Field()

