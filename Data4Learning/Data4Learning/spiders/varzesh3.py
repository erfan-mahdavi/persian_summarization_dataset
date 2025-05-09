import scrapy
from items import NewsItem
from spiders.base_spider import BaseSpider

class Varzesh3Spider(BaseSpider):
    name = "varzesh3"
    allowed_domains = ["varzesh3.com"]
    start_urls = ["https://varzesh3.com/news"]
    
    def start_requests(self):
        for i in range(1500000, 2120001):
                    url = (
                        f"https://www.varzesh3.com/news/{i}"
                    )
                    yield scrapy.Request(
                        url,
                        callback=self.parse_article,
                        errback=self.errback,
                        priority=10,
                    )



    def parse_article(self, response):
        title = self.clean_text(response.css('h1.headline::text').get())
        category = ''
        tags = self.clean_tags(response.css('div.tags.tags-news a ::text').getall())
        article = self.clean_nodes(response.css('div.news-text p ::text').getall())
        link = response.url
        
        if title and len(article) > 10 and ("varzesh3.com/news" in link) :
            item = NewsItem(
                title=title,
                article=article,
                summary=self.clean_text(response.css('p.lead::text').get()),
                category=category,
                tags=tags,
                network=self.name,
                link=link
            )
            yield item