import scrapy
from items import NewsItem
from spiders.base_spider import BaseSpider

class BazicenterNewsSpider(BaseSpider):
    name = "bazicenter_news"
    allowed_domains = ["bazicenter.com"]
    start_urls = ["https://www.bazicenter.com/category/news/"]


    def __init__(self, *args, **kwargs):
        super(BazicenterNewsSpider, self).__init__(*args, **kwargs)
        self.counter = 1


    def parse_main(self, response):
        pages = response.css('h2.post-title a::attr(href)').getall()
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
        next_page_url = f"https://www.bazicenter.com/category/news/page/{self.counter}/"

        if self.counter <= 5000: 
            yield scrapy.Request(
                url=next_page_url,
                callback=self.parse_main,
                errback=self.errback,
                priority=4
            )

    def parse_article(self, response):
        title = self.clean_text(response.css('h1.post-title.entry-title::text').get())
        category = ''
            
        tags = self.clean_tags(response.css('span.tagcloud a ::text').getall())
        article = self.clean_nodes(response.css('div.entry-content p ::text').getall())

        if title and len(article) > 10:
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