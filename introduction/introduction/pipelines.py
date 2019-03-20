# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from .items import BlogItem


# 存储自己的数据
class IntroductionPipeline(object):

    def process_item(self, item, spider):

        if isinstance(item, BlogItem):
            print('got an blog : {}'.format(item))
        return item
