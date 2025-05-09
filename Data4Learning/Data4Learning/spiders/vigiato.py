import scrapy
from items import NewsItem
from spiders.base_spider import BaseSpider

class VigiatoSpider(BaseSpider):
    name = "vigiato"
    allowed_domains = ["vigiato.net"]
    start_urls = ["https://vigiato.net/c/game-reviews"]

    def __init__(self, *args, **kwargs):
        super(VigiatoSpider, self).__init__(*args, **kwargs)
        self.counter = 1


    def parse_main(self, response):
        pages = response.css('div.todaysNewsList[id="todaysNews"] h2 a::attr(href)').getall()
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
        next_page_url = f"https://vigiato.net/c/game-reviews/page/{self.counter}"

        if self.counter <= 5000: 
            yield scrapy.Request(
                url=next_page_url,
                callback=self.parse_main,
                errback=self.errback,
                priority=4
            )

    def parse_article(self, response):
        title = self.clean_text(response.css('h1.dailyNewsPageHead__description--title::text').get())
        category = 'نقد و بررسی بازی'
            
        tags = self.clean_tags(response.css('div.postTools__keywords a::text').getall())
        if not tags:
            tags = self.clean_tags(response.css('div.customRow span > ::text').getall())
        article = self.clean_nodes(response.css('div.articleContent p ::text').getall())
        if title and len(article) > 10 and tags:
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