import scrapy
from items import NewsItem
from spiders.base_spider import BaseSpider

class MeydannewsSpider(BaseSpider):
    name = "meydannews"
    allowed_domains = ["meydannews.com"]
    start_urls = ["https://meydannews.com/fa/archive"]

    def parse_main(self, response):
        pages = response.css('ul.linear_news_sections li.linear_news_sec a.txt::attr(href)').getall()
        for href in pages:
            url = "https://meydannews.com" + href
            if self.allowed_domains[0] in url:
                yield scrapy.Request(
                    url,
                    callback=self.parse_article,
                    errback=self.errback,
                    priority = 5
                )
        navs = response.css('a.next[title="next"]::attr(href)').get()
        if navs:
            next = navs
            url = "https://meydannews.com" + next
            if self.allowed_domains[0] in url:
                yield scrapy.Request(
                    url,
                    callback=self.parse_main,
                    errback=self.errback,
                    priority = 4
                )
    
    def parse_article(self, response):
        title = self.clean_text(response.css('h1.main_news_title ::text').get())
        categories = (response.css('div.news_path a::text').getall())
        if categories:
            category = categories[-1]
        else:
            category = ''
            
        tags = self.clean_tags(response.css('div.tags_items a.tags_item::text').getall())
        article = self.clean_nodes(response.css('div.body p ::text').getall())

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
