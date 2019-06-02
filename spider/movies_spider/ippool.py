# -*- coding: utf-8 -*-
import random
# 导入settings.py中的IPPOOL
from .settings import IPPOOL
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware


class ippool(HttpProxyMiddleware):

    def __init__(self, ip=''):
        self.ip = ip

    def process_request(self, request, spider):
        ip = random.choice(IPPOOL)
        print("当前使用IP是：" + ip)
        request.meta["proxy"] = ip
