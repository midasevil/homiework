#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from random import choice

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
            print('=============================',request.headers['User-Agent'],'======================================')


#TODO(midasevil) class RotateProxyMiddleware(object):















