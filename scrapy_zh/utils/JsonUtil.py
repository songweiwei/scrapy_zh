#! /usr/bin/env python
# -*- coding: utf-8 -*-
from scrapy_zh import config
import os
import json
import logging

class JsonUtil(object):

    def jsonUnion(self, jsonPath, jsonDataFile):
        '''
        将多个Json文件去重合并生成目标文件
        :param jsonPath: 需要合并的json文件目录, news-*.json
        :param jsonFileName: 生成的json目标文件news.json
        :return: None
        '''
        # 获取new-*.json文件列表，将数据合并去重
        logging.info("开始合并new-*.json文件")
        jsonMaps = {}
        jsonFiles = os.listdir(jsonPath)
        for fileName in jsonFiles:
            jsonFile = os.path.join(jsonPath, fileName)
            with open(jsonFile, 'r', encoding='utf-8') as fp:
                jsonNews = json.load(fp)
                for jsonNew in jsonNews:
                    jsonMaps[jsonNew['url']] = jsonNew
            logging.info('完成fileName=%s数据合并' %(fileName))
        jsonList = []
        for jsonMap in jsonMaps.values():
            jsonList.append(jsonMap)

        # 将去合并去重数据保存到目标文件news.json
        with open(config.spiderDataFile, 'w', encoding='utf-8') as fp:
            json.dump(jsonList, fp, ensure_ascii=False, indent=4)
        logging.info("完成new-*.json文件，目标文件保存【%s】" %(config.spiderDataFile))

if __name__ == '__main__':
    jsonPath = config.spiderDataPath
    jsonDataFile = config.spiderDataFile
    jsonUtil = JsonUtil()

    jsonUtil.jsonUnion(jsonPath, jsonDataFile)