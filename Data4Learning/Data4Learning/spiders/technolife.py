import scrapy
from items import NewsItem
from spiders.base_spider import BaseSpider

class TechnolifeSpider(BaseSpider):
    name = "technolife"
    allowed_domains = ["technolife.com"]
    start_urls = ["https://www.technolife.com/blog/review/"]



    def __init__(self, *args, **kwargs):
        super(TechnolifeSpider, self).__init__(*args, **kwargs)
        self.counter = 2


    def parse_main(self, response):
        pages = response.css('div.mobile-review-item h3.mobile-review-item-title a::attr(href)').getall()
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
        next_page_url = f"https://www.technolife.com/blog/review/page/{self.counter}/"

        if self.counter <= 5000: 
            yield scrapy.Request(
                url=next_page_url,
                callback=self.parse_main,
                errback=self.errback,
                priority=4
            )

    def parse_article(self, response):
        title = self.clean_text(response.css('h1.post-item-title::text').get())
        categories = response.css('div.breadcrumbs li a::text').getall()
        if categories:
            category = self.clean_text(categories[-2])
        tags = self.clean_tags(response.css('div.post-tags a::text').getall())
        article = self.clean_nodes(response.css('div.post-container p ::text, div.post-container h2 ::text').getall())
        if article[-120:].find("در این مطلب") != -1:  
                article = article[:article.rfind("در این مطلب")] 
        if title and len(article) > 10 and category:
            item = NewsItem(
                title=title,
                article=article,
                summary='',
                category=category,
                tags=f'{category},نقد و بررسی تکنولوژی',
                network=self.name,
                link=response.url
            )
            yield item