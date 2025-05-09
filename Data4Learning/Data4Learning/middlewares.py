# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from itemadapter import is_item, ItemAdapter
from scrapy.exceptions import IgnoreRequest
import logging
from collections import defaultdict
from datetime import datetime, timedelta
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.exceptions import IgnoreRequest

class CustomRetryMiddleware(RetryMiddleware):
    @classmethod
    def from_crawler(cls, crawler):
        # scrapy calls this to create your middleware
        return cls(crawler.settings)

    def __init__(self, settings):
        super().__init__(settings)
        # ignore Retry-After headers so we don’t pause the slot for 300s
        self._respect_retry_after_header = False


class Data4LearningSpiderMiddleware:
    """Default spider middleware scaffold."""
    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        return None

    def process_spider_output(self, response, result, spider):
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # You may handle exceptions here
        pass

    def process_start_requests(self, start_requests, spider):
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info(f"Spider opened: {spider.name}")

class Data4LearningDownloaderMiddleware:
    """Default downloader middleware scaffold."""
    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        return None

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        pass

    def spider_opened(self, spider):
        spider.logger.info(f"Spider opened: {spider.name}")

class ErrorLoggingMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    def process_spider_exception(self, response, exception, spider):
        spider.logger.error(f"Error at {response.url}: {exception}")
        return []
