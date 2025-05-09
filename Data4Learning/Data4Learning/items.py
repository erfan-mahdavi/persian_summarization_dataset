# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsItem(scrapy.Item):
    title    = scrapy.Field()
    article  = scrapy.Field()
    summary  = scrapy.Field()
    category = scrapy.Field()
    tags     = scrapy.Field()
    network  = scrapy.Field()
    link     = scrapy.Field()
