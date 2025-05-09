import scrapy
from items import NewsItem
from spiders.base_spider import BaseSpider

class DigiatoSpider(BaseSpider):
    name = "digiato"
    allowed_domains = ["digiato.com"]
    start_urls = ["https://digiato.com/daily-timeline"]

    def __init__(self, *args, **kwargs):
        super(DigiatoSpider, self).__init__(*args, **kwargs)
        self.counter = 1


    def parse_main(self, response):
        pages = response.css('div.rowCard a::attr(href)').getall()
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
        next_page_url = f"https://digiato.com/daily-timeline/page/{self.counter}"

        if self.counter <= 7000: 
            yield scrapy.Request(
                url=next_page_url,
                callback=self.parse_main,
                errback=self.errback,
                priority=4
            )

    def parse_article(self, response):
        title = self.clean_text(response.css('h1.dailyNewsPageHead__description--title::text').get())
        categories = response.css('div.breadcrumb ul.list-unstyled a::text').getall()
        if categories:
            category = self.clean_text(categories[-1])
        tags = self.clean_tags(response.css('div.postTools__keywords a::text').getall())
        article = self.clean_nodes(response.css('div.articlePost p ::text').getall())
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