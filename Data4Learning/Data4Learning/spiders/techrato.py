import scrapy
from items import NewsItem
from spiders.base_spider import BaseSpider

class TechratoSpider(BaseSpider):
    name = "techrato"
    allowed_domains = ["techrato.com"]
    start_urls = ["https://techrato.com"]

    def __init__(self, *args, **kwargs):
        super(TechratoSpider, self).__init__(*args, **kwargs)
        self.counter = 1


    def parse_main(self, response):
        pages = response.css('div.clearfix a.title::attr(href)').getall()
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
        next_page_url = f"https://techrato.com//page/{self.counter}/"

        if self.counter <= 5900: 
            yield scrapy.Request(
                url=next_page_url,
                callback=self.parse_main,
                errback=self.errback,
                priority=4
            )

    def parse_article(self, response):
        title = self.clean_text(response.css('h1[itemprop="headline"]::text').get())
        categories = response.css('ul.post-categories a::text').getall()
        tags = response.css('div.tags-nav ::text').getall()
        tags = self.clean_tags(categories+tags)
        article = self.clean_nodes(response.css('div.content[itemprop="articleBody"] p ::text').getall())
        if title and len(article) > 10 and tags:
            item = NewsItem(
                title=title,
                article=article,
                summary='',
                category='اخبار تکنولوژي',
                tags=tags,
                network=self.name,
                link=response.url
            )
            yield item