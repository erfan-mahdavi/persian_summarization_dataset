import scrapy
from items import NewsItem
from spiders.base_spider import BaseSpider

class GamefaSpider(BaseSpider):
    name = "gamefa"
    allowed_domains = ["gamefa.com"]
    start_urls = ["https://gamefa.com/category/game/page/2/"]

    def __init__(self, *args, **kwargs):
        super(GamefaSpider, self).__init__(*args, **kwargs)
        self.counter = 2


    def parse_main(self, response):
        pages = response.css('div.col-12 a.d-block::attr(href)').getall()
        for href in pages:
            url = href
            if self.allowed_domains[0] in url:
                yield scrapy.Request(
                    url,
                    callback=self.parse_article,
                    errback=self.errback,
                    priority=5
                )
        

        self.counter += 1
        next_page_url = f"https://gamefa.com/category/game/page/{self.counter}"

        if self.counter <= 5000: 
            yield scrapy.Request(
                url=next_page_url,
                callback=self.parse_main,
                errback=self.errback,
                priority=4
            )

    def parse_article(self, response):
        title = self.clean_text(response.css('h1.post-title::text').get())
        categories = response.css('span.aioseo-breadcrumb a::text').getall()
        if categories:
            category = categories[-1]
        tags = self.clean_tags(response.css('div.post-tags a::text').getall())
        article = self.clean_nodes(response.css('div.post-content p ::text').getall())
        if title and len(article) > 10 and category:
            item = NewsItem(
                title=title,
                article=article,
                summary='',
                category=category,
                tags=tags,
                network=self.name,
                link=response.url
            )
            yield item