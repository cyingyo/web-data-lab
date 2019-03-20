# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import scrapy


# 定义一些字段，这些字段用来临时存储你需要保存的数据。方便后面保存数据到其他地方.
# 比如数据库 或者 本地文本之类的。
class BlogItem(scrapy.Item):
    title = scrapy.Field()
