# -*- coding: utf-8 -*-
import scrapy
from ..items import *

class Douban250Spider(scrapy.Spider):
    name = 'douban250'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/top250/']

    def parse(self, response):
        # 获取当前页列表
        movie_list = response.xpath('//div[@class="article"]//ol[@class="grid_view"]//li//div[@class="item"]')
        for i in movie_list:
            items = DoubanTop250Item()
            items['serial_number'] = i.xpath('.//em/text()').extract_first()
            items['name'] = i.xpath('.//span[@class="title"]/text()').extract_first()
            items['stars'] = i.xpath('.//div[@class="star"]//span/text()').extract()
            items['quote'] = i.xpath('.//p[@class="quote"]//span[@class="inq"]/text()').extract_first()
            #  这里内容较多，需要特殊处理
            items['introduce'] = []
            content = i.xpath('.//p[@class=""]/text()').extract()
            for t in content:  # 去空格
                # items['introduce'] = "".join(t.split())  # 输出的时候只有年份分类，没有了导演演员，猜测是for的时候替换掉了
                # items['introduce'].append(t.split())  # 字典键值对不能这样搞，也不能=[].append()，还是会替换掉，傻逼
                items['introduce'].append("".join(t.split()))
            print(items)
            yield items  # 存入pipelines

        next_link = response.xpath('//span[@class="next"]//a/@href').extract_first()
        if next_link:  # 如果有内容
            next_link = scrapy.Request("https://movie.douban.com/top250"+next_link, callback=self.parse)
            yield next_link
