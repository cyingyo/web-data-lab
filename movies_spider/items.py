# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class DoubanMoviesItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = Field()
    title = Field()
    rate = Field()
    cover = Field()
    directors = Field()
    casts = Field()
    description = Field()
    url = Field()
    year = Field()
    comments = Field()


class MaoyanMoviesItem(Item):
    id = Field()
    title = Field()
    rate = Field()
    piaofang = Field()
    cover = Field()
    directors = Field()
    casts = Field()
    description = Field()
    year = Field()
    comments = Field()

