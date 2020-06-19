#! /usr/bin/env python
# -*- coding: utf-8 -*-
from scrapy_zh.config import mongodbConfig, spiderDataFile
import pymongo
import json
import logging


class MongoUtil(object):
    def __init__(self):
        mongoUrl = self.getMongoUrl()
        self.mongoclient = pymongo.MongoClient(mongoUrl)
        self.mongoDB = self.mongoclient.yuqingdb

    def getMongoUrl(self):
        '''
        获取mongo url
        :return:
        '''
        mongoUrl = 'mongodb://' + mongodbConfig['username'] + ':' + mongodbConfig['password']+ '@' + \
                   mongodbConfig['host'] +'/' + mongodbConfig['database']
        return mongoUrl

    def inserJson(self, jsonDataFile):
        logging.info('开始插入Json数据到Mongdb')
        with open(jsonDataFile, 'r', encoding='utf-8') as fp:
            jsonData = json.load(fp)
            self.mongoDB[mongodbConfig['newsCol']].insert(jsonData)
        logging.info('完成插入Json数据到Mongdb')

    def close(self):
        self.mongoclient.close()

if __name__ == '__main__':
    mongoUtil = MongoUtil()
    mongoUtil.inserJson(spiderDataFile)