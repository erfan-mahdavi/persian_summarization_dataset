import scrapy
from items import NewsItem
from spiders.base_spider import BaseSpider

class TarafdariSpider(BaseSpider):
    name = "tarafdari"
    allowed_domains = ["tarafdari.com"]
    start_urls = ["https://www.tarafdari.com/static/page/archive"]

    def parse_main(self, response):
        pages = response.css('a.title-node-custom-class::attr(href)').getall()
        for href in pages:
            url = "https://www.tarafdari.com" + href
            if self.allowed_domains[0] in url:
                yield scrapy.Request(
                    url,
                    callback=self.parse_article,
                    errback=self.errback,
                    priority = 5
                )
        navs = response.css('li.pager-next a::attr(href)').get()
        if navs:
            next = navs
            url = "https://www.tarafdari.com" + next
            if self.allowed_domains[0] in url:
                yield scrapy.Request(
                    url,
                    callback=self.parse_main,
                    errback=self.errback,
                    priority = 4
                )
    
    def parse_article(self, response):
        title = self.clean_text(response.css('h1.node__title::text').get())
        categories = response.css('span.bread_path a::text').getall()
        category = ''
            
        tags = self.clean_tags(response.css('div.field.field-name-field-category div.field-items div.field-item a::text').getall()+response.css('div.field.field-name-field-tags div.field-items div.field-item a::text').getall())
        article = self.clean_nodes(response.css('div.field.field-name-body div.field-items div.field-item p ::text').getall())

        if title and len(article)>10 and tags:
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
