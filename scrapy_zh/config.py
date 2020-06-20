#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, time

projectPath = os.path.dirname(os.path.abspath(__file__))
nowDate = time.strftime('%Y%m%d', time.localtime())
spiderDataPath = projectPath + r'/spider_datas/' + nowDate
spiderDataFile = spiderDataPath + r'/news.json'



# 爬取最大页数
maxPageNum = 10

# 爬取增量天数
crawlIncDays = 20


# 检索关键字
key_word=["医疗","卫生","健康","就医","看病","医生","护士","药品","医院","医保","挂号","买药"]
loc_word=["广东","珠海"]
keyWords=[" ".join([i,j]) for i in loc_word for j in key_word]
# keyWords=[
#     '医疗 人民网',
#     '医疗 珠海'
# ]


# url白名单
white_url_dict={
    "百度资讯":"http://www.baidu.com",
    "腾讯新闻":"https://new.qq.com",
    "搜狐网":"http://www.souhu.com",
    "搜狐网移动":"https://m.sohu.com/",
    "搜狐网经济http":"http://finance.sina.com.cn/",
    "搜狐网经济https":"https://finance.sina.com.cn/",
    "南方新闻网": "http://news.southcn.com",
    "南方中文网":"http://zh.southcn.com/",
    "南方快报":"http://kb.southcn.com/",
    "澎湃新闻": "http://www.thepaper.cn",
    "港澳在线": "http://www.gangaonet.cn",
    "金羊网": "http://www.ycwb.com",
    "网易新闻移动端":"https://3g.163.com",
    "网易新闻":"http://news.163.com",
    "潇湘晨报":"http://www.xxcb.com",
    "人民网":"http://fj.people.com.cn"
}
whiteUrls=list(white_url_dict.values())

# mongodb config
mongodbConfig = {
    'host': '172.16.40.154',
    'port': 27017,
    'username': 'yuqing',
    'password': 'yuqing#123',
    'database': 'yuqingdb',
    'newsCol': 'yuqing_news'
}