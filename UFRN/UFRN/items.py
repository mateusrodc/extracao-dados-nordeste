# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class UfrnItem(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()    
    keywords = scrapy.Field()
    date = scrapy.Field()
    abstract = scrapy.Field()
    uri = scrapy.Field()
    type = scrapy.Field()
    
    pass
