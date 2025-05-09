import scrapy
from items import NewsItem
from spiders.base_spider import BaseSpider

class DigikalaGameSpider(BaseSpider):
    name = "digikala_game"
    allowed_domains = ["digikala.com"]
    start_urls = ["https://www.digikala.com/mag/category/%D8%A8%D8%A7%D8%B2%DB%8C/page/1/"]


    def __init__(self, *args, **kwargs):
        super(DigikalaGameSpider, self).__init__(*args, **kwargs)
        self.counter = 1


    def parse_main(self, response):
        pages = response.css('div.masonry-gallery__item a.masonry-gallery__item__title::attr(href)').getall()
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
        next_page_url = f"https://www.digikala.com/mag/category/%D8%A8%D8%A7%D8%B2%DB%8C/page/{self.counter}/"

        if self.counter <= 5900: 
            yield scrapy.Request(
                url=next_page_url,
                callback=self.parse_main,
                errback=self.errback,
                priority=4
            )

    def parse_article(self, response):
        title = self.clean_text(response.css('h1._txt.entry-title::text').get())
        categories = response.css('ul.breadcrumbs__nav li.item a::text').getall()
        category = ''
        if categories:
            category = self.clean_text(categories[-1])
        tags = self.clean_tags(response.css('div.post-module__tags a.post-tag::text').getall())
        article = self.clean_nodes(response.xpath(
    '//div[contains(@class, "post-module__content")]//p[not(ancestor::section[contains(concat(" ", normalize-space(@class), " "), " wrapper-dkmag-review-article ")])]/text()'
    ' | '
    '//div[contains(@class, "post-module__content")]//h2[not(ancestor::section[contains(concat(" ", normalize-space(@class), " "), " wrapper-dkmag-review-article ")])]/text()'
).getall()
) 
        if article[-30:].find("منبع") != -1:  
                article = article[:article.rfind("منبع")] 
        
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