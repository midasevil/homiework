# -*- coding: utf-8 -*-
from datetime import datetime


class jinSPipeline(object):
    """nothing new"""
    def process_item(self, item, spider):
        item["jcrawled"] = datetime.now()
        item["jspider"] = spider.name
        return item



