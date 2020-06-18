# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsItem(scrapy.Item):
    title = scrapy.Field()
    publish_date = scrapy.Field()
    url = scrapy.Field()
    source_media = scrapy.Field()
    spread_media = scrapy.Field()
    content = scrapy.Field()
    content_html = scrapy.Field()
    spider_data_file = scrapy.Field()


