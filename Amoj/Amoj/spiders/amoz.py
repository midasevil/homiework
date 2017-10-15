#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import scrapy
from lxml import etree
import re
from Amoj.items import AmozItem
from urllib.request import quote, unquote
from .util import safeget, info_to_dict


p1 = re.compile(r'https://www.amazon.cn/(.*?)/dp/(.*?)/')
p2 = re.compile(r'https://www.amazon.cn/dp/(.*?)/')


class AmozSpider(scrapy.Spider):
    name = 'amoj'
    start_urls = [
        'https://www.amazon.cn/gp/search/other/ref=sr_sa_p_lbr_one_browse-bin?rh=n%3A658390051&bbn=658390051&pickerToList=lbr_one_browse-bin&ie=UTF8&qid=1507877308'

    ]

    def parse(self, response):
        """find first index page with same authors """
        html = etree.HTML(response.text)
        hrefs = html.xpath('//li/span/a[@class="a-link-normal"]/@href')
        for url in hrefs:
            if url:
                yield response.follow(url, callback=self.parse_item)


    def parse_item(self, response):
        """find every book info and next page following"""
        html = etree.HTML(response.text)
        items = html.xpath('//li[@id]')

        for item in items:
            amozitem = AmozItem()
            href = item.xpath(
                './/a[@class="a-link-normal s-access-detail-page  s-color-twister-title-link a-text-normal"]/@href')
            href = safeget(href, 0)
            if p1.findall(href):
                title_url, pid = safeget(p1.findall(href), 0)
                title_url = safeget(title_url.split('-', 1), 0)
                if title_url == '%E5%9B%BE%E4%B9%A6':
                    title_cn = safeget(item.xpath('.//h2[@data-attribute]/text()'), 0)
                else:
                    title_cn = unquote(title_url)
            else:
                pid = safeget(p2.findall(href), 0)
                title_cn = safeget(item.xpath('.//h2[@data-attribute]/text()'), 0)
            info = item.xpath('.//text()')
            info_dict = info_to_dict(info)
#            info_dict.update({'title_cn': title_cn, 'pid': pid})
            amozitem['pid'] = pid
            amozitem['hardcover'] = info_dict['hardcover']
            amozitem['papercover'] = info_dict['papercover']
            amozitem['morechoices'] = info_dict['morechoices']
            amozitem['title'] = title_cn
            amozitem['kindle'] = info_dict['kindle']
            amozitem['comments'] = info_dict['comments']

            yield amozitem

        next_page = html.xpath('//span[@class="pagnRA"]/a[@title="下一页"]/@href')
        if not len(next_page) == 0:
            yield response.follow(next_page[0], callback=self.parse_item)







