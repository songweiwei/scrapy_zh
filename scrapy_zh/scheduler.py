#! /usr/bin/env python
# -*- coding: utf-8 -*-


from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy_zh.utils.JsonUtil import JsonUtil
from scrapy_zh.utils.MongoUtil import MongoUtil
from scrapy_zh import config
import logging


def runSpider(spider):
    '''
    安装关键字启动N个爬虫程序
    :param spider:
    :return:
    '''
    process = CrawlerProcess(get_project_settings())

    for i in range(len(config.keyWords)):
        keyWord = config.keyWords[i]
        spiderDataFile = 'news-' + str(i+1) + '.json'
        process.crawl(spider, keyWord=keyWord, spiderDataFile=spiderDataFile)
    process.start()



if __name__ == '__main__':
    # 1、增量爬取数据
    logging.info('启动爬虫程序...')
    runSpider('baidu_spider')
    logging.info('完成爬虫程序...')

    # 2、将爬虫落地的文件Json数据进行去重合并
    logging.info('启动Json数据合并程序...')
    jsonUtil = JsonUtil()
    jsonUtil.jsonUnion(config.spiderDataPath, config.spiderDataFile)
    logging.info('完成Json数据合并程序...')

    # 3、将数据加载到Mongo数据库中
    logging.info('启动数据插入Mongdb程序...')
    mongoUtil = MongoUtil()
    mongoUtil.inserJson(config.spiderDataFile)
    logging.info('完成数据插入Mongdb程序...')




