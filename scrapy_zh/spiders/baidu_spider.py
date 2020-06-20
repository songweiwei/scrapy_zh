#! /usr/bin/env python
# -*- coding: utf-8 -*-

import re
import datetime
from scrapy_zh.items import *
from urllib import parse
from pydispatch import dispatcher
from scrapy import signals
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from scrapy_zh.settings import DEFAULT_BROWSER
from gne import GeneralNewsExtractor
from scrapy_zh import config
import logging
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options

# #一下三行为无头模式运行，无头模式不开启浏览器，也就是在程序里面运行的
chrome_options = Options()
chrome_options.add_argument("--headless")



class BaiduSpider(scrapy.Spider):
    name = 'baidu_spider'
    domain = 'baidu.com'
    start_url = 'https://www.baidu.com/s'
    # 定义浏览器的相关性能：这里设置为无图浏览
    chrome_opt = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_opt.add_experimental_option("prefs", prefs)
    chrome_opt.add_argument('--headless')
    # 翻页信息
    pageNum = 1
    pageCount = 1
    # 爬虫数据保存文件
    spiderDataFile = None
    # 爬虫增量停止标志
    scrawStopFlag = False

    key_word = '医疗 人民网'

    search_data = {
        "wd": key_word,
        "cl": 2,
        "tn": "news",   # 资讯
        "rtt": 4,      # 按时间倒序
        "pn": 0
    }

    def __init__(self, keyWord=None, spiderDataFile=None):
        # 初始化
        super(BaiduSpider, self).__init__()
        # 选择 不同的模拟浏览器
        if DEFAULT_BROWSER == 'Chrome':
            self.browser = webdriver.Chrome(chrome_options=self.chrome_opt)
        elif DEFAULT_BROWSER == 'PhantomJS':
            self.browser = webdriver.PhantomJS()
        # 规划自定义 browser大小
        self.browser.set_window_size(700, 700)
        # 设置启动延时
        self.wait = WebDriverWait(self.browser, 5)
        # spider关闭信号和spider_spider_closed函数绑定
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        # 设置爬取关键字
        self.key_word = keyWord
        # 设置爬取数据保存文件名称
        self.spiderDataFile = spiderDataFile

    def spider_closed(self):
        self.browser.close()

    def start_requests(self):
        logging.info("start request keyword=%s, spiderDataFile=%s" %(self.key_word, self.spiderDataFile))
        self.search_data['wd'] = self.key_word
        url_data = parse.urlencode(self.search_data, encoding='gbk')
        url = '{}?{}'.format(self.start_url, url_data)
        print(url)
        request = scrapy.Request(url=url, callback=self.parse)
        yield request

    def parse(self, response):
        logging.info("**start parse, keyword=%s pageNum=%d" %(self.key_word, self.pageNum))
        article_url_list = response.xpath('//*[@id="content_left"]/div/div[@class="result"]')
        for i in range(len(article_url_list)):
            article_url_obj = article_url_list[i]
            article_title = article_url_obj.xpath('./h3//text()').getall()
            article_title = ''.join(article_title)
            article_title = re.sub('\s','',article_title)
            article_url = article_url_obj.xpath('./h3/a/@href').extract_first()
            article_source_str = article_url_obj.xpath('./div//p//text()').getall()
            article_source_str = ''.join(article_source_str)
            # 将所有的空白符替换成空格，并去除前后空格
            article_source_str = re.sub('\s', ' ', article_source_str).strip()
            # 将网站来源和时间中间的所有字符用一个字符替代
            article_source_str = re.sub(' +', ' ', article_source_str)
            article_source_arr = article_source_str.split(' ')
            article_source = ''
            article_publish_date = ''
            # 将新闻来源和时间进行分割
            if len(article_source_arr) >= 2:
                article_source = article_source_arr[0]
                article_publish_date = article_source_arr[1]

            # 退出判断，当新闻发布日期大于增量天数，则终止爬取
            # 获取增量的最小日期， 按照增量的时间段往前推，找到最小的增量时间
            currentDate = datetime.datetime.now()
            dateDelta = datetime.timedelta(days=config.crawlIncDays * -1)
            minCrawlDate = currentDate + dateDelta
            minIncCrawDate = minCrawlDate.strftime('%Y-%m-%d')

            # 目前的首页抓取的日期有两种格式
            # 格式1：N小时前   格式2：N分钟前 格式3：2020年06月08日 14:15
            # match1 = re.findall('\d+小时前', article_publish_date)
            match2 = re.findall('(\d+)年(\d+)月(\d+)日', article_publish_date)
            page_info = 'pageNum={}, pageCount={}'.format(self.pageNum, self.pageCount)
            # N小时前 或者 新闻日期>=最小增量爬虫日期
            if (len(match2)==0 and self.urlFilter(article_url)) or (len(match2)>0 and self.urlFilter(article_url) and '-'.join(match2[0]) >= minIncCrawDate):
            # if (len(match2) == 0 or (len(match2) > 0) and self.urlFilter(article_url) and '-'.join(match2[0]) >= minIncCrawDate):
                logging.info('%s\t%s\t%s\t%s\t%s' %(page_info, article_title , article_url, article_source , article_publish_date))
                request = scrapy.Request(url = article_url, callback= self.parse_item)
                request.meta['title'] = article_title
                request.meta['url'] = article_url
                request.meta['source_media'] = article_source
                request.meta['publish_date'] = article_publish_date
                yield request
            else:
                self.scrawStopFlag = True
                logging.info('停止爬取数据-%s\t%s\t%s\t%s\t%s' %(page_info, article_title , article_url, article_source , article_publish_date))

            # 页面数 + 1
            self.pageCount += 1

        # 翻页数 + 1
        self.pageNum += 1

        # 下一页判断
        next_page_names = response.xpath('//*[@id="page"]/a/text()').getall()
        # 存在下一页 + 不超过最大爬取页数 + 增量Stop标识为False
        if '下一页>' in next_page_names and self.pageNum <= config.maxPageNum and self.scrawStopFlag==False:
            logging.info('pageNum=%d' %(self.pageNum))
            self.search_data['pn'] = (self.pageNum - 1) * 10
            url_data = parse.urlencode(self.search_data,encoding='gbk')
            url = '{}?{}'.format(self.start_url, url_data)
            request = scrapy.FormRequest(url=url, callback=self.parse)
            logging.info(url)
            yield request

    def parse_item(self, response):
        '''
        解析文章内容
        :param response:
        :return: 返回数据Item对象
        '''

        exetractor = GeneralNewsExtractor()
        # logging.info(response.text)
        newInfo = exetractor.extract(response.text, title_xpath='//h5/text')
        item = NewsItem()
        item['title'] = response.meta['title']
        item['publish_date'] = newInfo['publish_time']
        item['url'] = response.meta['url']
        item['source_media'] = response.meta['source_media']
        item['spread_media'] = ''
        item['content'] = newInfo['content'].replace('\n','')
        item['content_html'] = ''
        item['spider_data_file'] = self.spiderDataFile
        yield item


    def urlFilter(self, url):
        '''
        白名单过滤
        :param url:
        :return: True 允许爬取， False：不允许爬取
        '''
        # filterFlag = True

        filterFlag = False
        for whiteUrl in config.whiteUrls:
            match = re.findall(whiteUrl, url)
            if len(match) > 0:
                filterFlag = True
                break

        return filterFlag

