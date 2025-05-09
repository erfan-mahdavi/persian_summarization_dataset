# Scrapy settings for Data4Learning project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'Data4Learning'
SPIDER_MODULES = ['Data4Learning.spiders']
NEWSPIDER_MODULE = 'Data4Learning.spiders'
TWISTED_REACTOR = 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'
FEED_EXPORT_ENCODING = 'utf-8'

# Basic crawl config (defaults shown commented)
ROBOTSTXT_OBEY = False
CONCURRENT_REQUESTS = 32  # default: 16
CONCURRENT_REQUESTS_PER_DOMAIN = 64
DOWNLOAD_DELAY              = 0.2  
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 0.1
RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408]
AUTOTHROTTLE_MAX_DELAY = 10
RETRY_TIMES = 2
HTTPERROR_ALLOWED_CODES = [403,404]
DEPTH_LIMIT = 1000000
DOWNLOAD_TIMEOUT = 10

COOKIES_ENABLED = False
HTTPCACHE_ENABLED = False
HTTPCACHE_EXPIRATION_SECS = 86400

DUPEFILTER_CLASS = 'scrapy.dupefilters.RFPDupeFilter'
'''
FEEDS = {
    'csv_files/%(name)s_articles.csv': {
        'format': 'csv',
        'encoding': 'utf-8-sig',
        'fields': ['title','article','summary','category','tags','network','link'],
        'overwrite': True,
    },
}
'''

MYSQL_SETTINGS = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': '13833298405',
    'db': 'data4learning',
}

ITEM_PIPELINES = {
    'Data4Learning.pipelines.MySQLPipeline': 300,
}

# Spider & downloader middlewares (include default scaffolds)
SPIDER_MIDDLEWARES = {
    'Data4Learning.middlewares.Data4LearningSpiderMiddleware': 543,
}
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    'Data4Learning.middlewares.Data4LearningDownloaderMiddleware': 543,
    'Data4Learning.middlewares.CustomRetryMiddleware': 550,
    #'Data4Learning.middlewares.DomainRateLimiter': 100,
    'Data4Learning.middlewares.ErrorLoggingMiddleware': 500,
}

