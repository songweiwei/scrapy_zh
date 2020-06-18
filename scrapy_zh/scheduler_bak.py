#! /usr/bin/env python
# -*- coding: utf-8 -*-


from apscheduler.schedulers.blocking import BlockingScheduler
from flask_apscheduler import APScheduler
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import threading
import sys, os, time
import subprocess
import scrapy.crawler as crawler
from twisted.internet import reactor
from scrapy_zh import config
from multiprocessing import Queue, Process
from scrapy_zh.spiders import baidu_spider

# from crochet import setup
# setup()

def runSpider1(keyWord, spiderDataFile):
    def run():
        # process = CrawlerProcess(get_project_settings())
        # print(keyWord, spiderDataFile)
        # process.crawl('baidu_spider', keyWord=keyWord, spiderDataFile=spiderDataFile)
        # process.start()
        try:
            print(keyWord, spiderDataFile)
            runner = crawler.CrawlerRunner(get_project_settings())
            deferred = runner.crawl('baidu_spider', keyWord=keyWord, spiderDataFile=spiderDataFile)
            # deferred.addBoth(lambda _: reactor.stop())
            # reactor.run()
            runner.join()

        except Exception as e:
            pass
    # p = Process(target=run)
    # p.start()
    # p.join()
    run()

def runSpider2(spider):
    runner = crawler.CrawlerRunner(get_project_settings())

    for i in range(len(config.keyWords)):
        keyWord = config.keyWords[i]
        spiderDataFile = 'news-' + str(i+1) + '.json'
        runner.crawl(spider, keyWord=keyWord, spiderDataFile=spiderDataFile)
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())
    reactor.run()


def runSpider(spider):
    process = CrawlerProcess(get_project_settings())

    for i in range(len(config.keyWords)):
        keyWord = config.keyWords[i]
        spiderDataFile = 'news-' + str(i+1) + '.json'
        process.crawl(spider, keyWord=keyWord, spiderDataFile=spiderDataFile)
    process.start()



if __name__ == '__main__':
    # scheduler = BlockingScheduler()
    # scheduler.add_job(runSpider3, 'cron', hour=18, minute=23, args=['baidu_spider'])
    # scheduler.start()

    #
    # for i in range(len(config.keyWords)):
    #     keyWord = config.keyWords[i]
    #     spiderDataFile = 'news-' + str(i+1) + '.json'
    #     runSpider(keyWord, spiderDataFile)
    #     # time.sleep(30)


    runSpider('baidu_spider')



