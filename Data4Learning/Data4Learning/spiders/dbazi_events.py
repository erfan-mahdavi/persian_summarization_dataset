import scrapy
from items import NewsItem
from spiders.base_spider import BaseSpider

class DbaziEventsSpider(BaseSpider):
    name = "dbazi_events"
    allowed_domains = ["dbazi.com"]
    start_urls = ["https://www.dbazi.com/gaming-events/"]
    custom_settings = {
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36',
    }



    def __init__(self, *args, **kwargs):
        super(DbaziEventsSpider, self).__init__(*args, **kwargs)
        self.counter = 1


    def parse_main(self, response):
        pages = response.css('a.thumbnail-post-item::attr(href)').getall()
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
        next_page_url = f"https://www.dbazi.com/gaming-events/page/{self.counter}"

        if self.counter <= 5000: 
            yield scrapy.Request(
                url=next_page_url,
                callback=self.parse_main,
                errback=self.errback,
                priority=4
            )

    def parse_article(self, response):
        title = self.clean_text(response.css('h1.title-single-content::text').get())
        categories = response.css('nav.rank-math-breadcrumb a::text').getall()
        category = ''
        if categories:
            category = self.clean_text(categories[-1])
        tags = self.clean_tags(response.css('div.post-meta-bottom a::text').getall())
        article = self.clean_nodes(response.css('main.dbazi-single-post-content p ::text').getall())

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