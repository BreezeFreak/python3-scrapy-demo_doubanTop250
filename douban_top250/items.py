# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanTop250Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    serial_number = scrapy.Field()     # 序号
    name = scrapy.Field()       # 名称
    stars = scrapy.Field()      # 评分
    introduce = scrapy.Field()  # 介绍(导演/演员/年份/国家)
    quote = scrapy.Field()      # 引言
