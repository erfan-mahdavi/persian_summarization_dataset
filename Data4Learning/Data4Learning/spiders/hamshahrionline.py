import scrapy
from items import NewsItem
from spiders.base_spider import BaseSpider

class HamshahrionlineSpider(BaseSpider):

    name = "hamshahrionline"
    allowed_domains = ["hamshahrionline.ir"]
    start_urls = ["https://www.hamshahrionline.ir/archive"]

    def start_requests(self):
        
        for year in range(1394, 1405):
            for month in range(1, 13):
                    url = (
                        f"https://www.hamshahrionline.ir/archive?pi=1&ms=0&mn={month}"
                        f"&yr={year}"
                    )
                    yield scrapy.Request(
                        url,
                        callback=self.parse_archive,
                        errback=self.errback,
                        priority=10,
                        meta={"year": year, "month": month, "page": 1}
                    )

    def parse_archive(self, response):
        year = response.meta["year"]
        month = response.meta["month"]
        page = response.meta["page"]

        links = response.css('li.news div.desc a::attr(href)').getall()
        if not links:
            return  

        for href in links:
            url = response.urljoin(href)
            if self.allowed_domains[0] in url:
                yield scrapy.Request(
                    url,
                    callback=self.parse_article,
                    errback=self.errback,
                    priority=5
                )
                
        next_page = page + 1
        next_url = (
            f"https://www.hamshahrionline.ir/archive?pi={next_page}&ms=0&mn={month}&yr={year}"
        )
        yield scrapy.Request(
            next_url,
            callback=self.parse_archive,
            errback=self.errback,
            priority=4,
            meta={"year": year, "month": month, "page": next_page}
        )
    
    def parse_article(self, response):
        title = self.clean_text(response.css('h1.title a[itemprop="headline"]::text').get())
        categories = response.css('li.breadcrumb-item a::text').getall()
        if categories:
            category = self.clean_text(categories[-1])
        else:
            category = ''
            
        tags = self.clean_tags(response.css('section.box.tags li a::text').getall())
        article = self.clean_nodes(response.css('div.item-text[itemprop="articleBody"] ::text').getall())

        if title and len(article)>10 and category:
            item = NewsItem(
                title=title,
                article=article,
                summary=self.clean_text(response.css('p.introtext::text').get()),
                category=category,
                tags=tags,
                network=self.name,
                link=response.url
            )
            yield item

    
'''
def parse_main(self, response):
        pages = response.css('li.news div.desc a::attr(href)').getall()
        for href in pages:
            url = "https://www.hamshahrionline.ir" + href
            if self.allowed_domains[0] in url:
                yield scrapy.Request(
                    url,
                    callback=self.parse_article,
                    errback=self.errback,
                    priority = 5
                )
        navs = response.css('ul.pagination li.page-item a::attr(href)').getall()
        if navs:
            next = navs[-1]
            url = "https://www.hamshahrionline.ir" + next
            if self.allowed_domains[0] in url:
                yield scrapy.Request(
                    url,
                    callback=self.parse_main,
                    errback=self.errback,
                    priority = 4
                )
'''