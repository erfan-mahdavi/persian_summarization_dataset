import scrapy
from items import NewsItem
from spiders.base_spider import BaseSpider

class KhabarvarzeshiSpider(BaseSpider):
    name = "khabarvarzeshi"
    allowed_domains = ["khabarvarzeshi.com"]
    start_urls = ["https://www.khabarvarzeshi.com/archive"]

    def parse_main(self, response):
        pages = response.css('li.news div.desc a::attr(href)').getall()
        for href in pages:
            url = "https://www.khabarvarzeshi.com" + href
            if self.allowed_domains[0] in url:
                yield scrapy.Request(
                    url,
                    callback=self.parse_article,
                    errback=self.errback,
                    priority = 5
                )
        navs = response.css('ul.pagination li.page-item a::attr(href)').getall()
        if navs:
            next = navs[-1]
            url = "https://www.khabarvarzeshi.com" + next
            if self.allowed_domains[0] in url:
                yield scrapy.Request(
                    url,
                    callback=self.parse_main,
                    errback=self.errback,
                    priority = 4
                )
    
    def parse_article(self, response):
        title = self.clean_text(response.css('h1.first-title::text').get())
        category = self.clean_text(response.css('div.item-path ol.breadcrumb li.breadcrumb-item.active a::text').get())
        tags = self.clean_tags((response.css('section.box.tags li a[rel="tag"]::text').getall()))
        article = self.clean_nodes(response.css('div.item-body div.item-text[itemprop="articleBody"] p ::text').getall())
        if article[-120:].find("بیشتر بخوانید") != -1:  
                article = article[:article.rfind("بیشتر بخوانید")] 

        if title and len(article)>10 and category:
            item = NewsItem(
                title=title,
                article=article,
                summary=self.clean_text(response.css('strong.news_strong::text').get()),
                category=category,
                tags=tags,
                network=self.name,
                link=response.url
            )
            yield item
