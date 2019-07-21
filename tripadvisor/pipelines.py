# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


# the atabase is MONGO＿Ｄ

import pymongo
from scrapy.conf import settings

class TripadvisorPipeline(object):
    def __init__(self):
        #  connect to database
        self.client = pymongo.MongoClient(host=settings['MONGO_HOST'], port=settings['MONGO_PORT'])

        self.db = self.client[settings['MONGO_DB']]  #  get database name
        self.coll = self.db[settings['MONGO_COLL']]  # get  collection name

    def process_item(self, item, spider):
        postItem = dict(item)  # item transfer dict
        self.coll.insert(postItem)  #  insert to databse
        return item
