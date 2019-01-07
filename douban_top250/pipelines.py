# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

class DoubanTop250Pipeline(object):
    def __init__(self):
        host = "127.0.0.1"
        port = 27017
        dbname = "test"
        collection_name = "test1"
        client = pymongo.MongoClient(host,port)
        mydb = client[dbname]
        self.post = mydb[collection_name]

    def process_item(self, item, spider):
        data = dict(item)
        self.post.insert(data)
        return item
