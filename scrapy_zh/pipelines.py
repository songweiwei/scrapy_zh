# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json, os
from scrapy_zh import config


class NewsPipleline(object):
    def __init__(self):
        self.file_name = ''

        # 如果当天数据目录不存在，则进行创建
        if not os.path.exists(config.spiderDataPath):
            os.makedirs(config.spiderDataPath)
        # 打开文件

        self.data = []

    def process_item(self, item, spider):
        item_dict = dict()
        item_dict['title'] = item['title']
        item_dict['publish_date'] = item['publish_date']
        item_dict['url'] = item['url']
        item_dict['source_media'] = item['source_media']
        item_dict['spread_media'] = item['spread_media']
        item_dict['content'] = item['content']
        item_dict['content_html'] = item['content_html']
        self.file_name = config.spiderDataPath + '/' + item['spider_data_file']
        self.data.append(item_dict)

    def close_spider(self, spider):
        self.file_out = open(self.file_name, 'w', encoding='utf-8')
        json.dump(self.data, self.file_out, indent=4, ensure_ascii=False)
        self.file_out.close()