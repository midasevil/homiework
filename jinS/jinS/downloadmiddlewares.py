#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from random import choice
from scrapy_redis.pipelines import RedisPipeline
import urllib

class RotateUserAgentMiddleware(object):

    """     This middleware allows spiders can rotate their useragents    """

    def __init__(self, user_agents=None):
        self.user_agents = user_agents

    @classmethod
    def from_crawler(cls, crawler):
        o = cls(crawler.settings['USER_AGENTS'])
        return o

    def process_request(self, request, spider):
        if self.user_agents:
            user_agent = choice(self.user_agents)
            request.headers.setdefault(b'User-Agent', user_agent)


class RotateProxyMiddleware(object):
    def __init__(self, proxies = None):
        self.proxies = proxies

    @classmethod
    def from_crawler(cls, crawler):
        f = crawler.settings['PROXY_FILE']
        with open(f) as f:
            proxies = f.readlines()

        return cls(proxies)

    def process_request(self, request ,spider):
        proxy = choice(self.proxies)
        request.meta['proxy'] = proxy

    def process_response(self, request, response, spider):
        if response.status != 200:
            fail_proxy = request.meta['proxy']
            self.proxies.remove(fail_proxy)
            proxy = choice(self.proxies)
            request.meta['proxy'] = proxy
            return request
        return response
















