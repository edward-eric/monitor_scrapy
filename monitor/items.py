# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MonitorItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class registerItem(scrapy.Item):
    id = scrapy.Field()
    href = scrapy.Field()
    val = scrapy.Field()
    lastUpdated = scrapy.Field()
