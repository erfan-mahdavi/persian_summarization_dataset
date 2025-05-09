import scrapy
from items import NewsItem
from spiders.base_spider import BaseSpider

class IsnaSpider(BaseSpider):
    name = "isna"
    allowed_domains = ["isna.ir"]
    start_urls = ["https://www.isna.ir/fa/page/archive.xhtml"]
    custom_settings = {
         'COOKIES_ENABLED': True,
         'USER_AGENT': (
             'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
             'AppleWebKit/537.36 (KHTML, like Gecko) '
             'Chrome/112.0.0.0 Safari/537.36'
         ),
     }

                
    def start_requests(self):
        
        for year in range(1394, 1405):
            for month in range(1, 13):
                for day in range(1, 32):
                    url = (
                        f"https://www.isna.ir/page/archive.xhtml?mn={month}"
                        f"&wide=0&dy={day}&ms=0&pi=1&yr={year}"
                    )
                    yield scrapy.Request(
                        url,
                        callback=self.parse_archive,
                        errback=self.errback,
                        priority=10,
                        meta={"year": year, "month": month, "day": day, "page": 1}
                    )

    def parse_archive(self, response):
        year = response.meta["year"]
        month = response.meta["month"]
        day = response.meta["day"]
        page = response.meta["page"]

        links = response.css('div.desc a::attr(href)').getall()
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
            f"https://www.isna.ir/page/archive.xhtml?mn={month}"
            f"&wide=0&dy={day}&ms=0&pi={next_page}&yr={year}"
        )
        if next_page <=100:
            yield scrapy.Request(
                next_url,
                callback=self.parse_archive,
                errback=self.errback,
                priority=4,
                meta={"year": year, "month": month, "day": day, "page": next_page}
            )
    
    def parse_article(self, response):
        title = self.clean_text(response.css('h1.first-title::text').get())
        category = self.clean_text(response.css('li.active a::text').get())
        tags = self.clean_tags(response.css('a[rel="tag"]::text').getall())
        article = self.clean_nodes(response.css('div.item-text[itemprop="articleBody"] p ::text').getall())

        if title and len(article)>10 and category:
            item = NewsItem(
                title=title,
                article=article,
                summary=self.clean_nodes(response.css('p.summary[itemprop="description"]::text').getall()),
                category=category,
                tags=tags,
                network=self.name,
                link=response.url
            )
            yield item
        
'''
    def parse_category(self,response):
        category = response.css('div.service-menu li a::attr(href)').getall()
        for href in category:
            url = response.urljoin(href)
            if  self.allowed_domains[0] in url:
                yield scrapy.Request(
                    url,
                    callback=self.parse_sub_category,
                    errback=self.errback,priority = 8
                )
                
    def parse_sub_category(self,response):
        sub_category = response.css('div.desc a::attr(href)').getall()
        for href in sub_category:
            url = response.urljoin(href)
            if  self.allowed_domains[0] in url:
                yield scrapy.Request(
                    url,
                    callback=self.parse_article,
                    errback=self.errback,priority = 6
                )
    links = response.css('div.desc a::attr(href)').getall()
        for href in links:
            url = response.urljoin(href)
            if  self.allowed_domains[0] in url:
                yield scrapy.Request(
                    url,
                    callback=self.parse_article,
                    errback=self.errback,priority = 3
                )
    
    
    
    def parse_main(self, response):
        pages = response.css('div.desc a::attr(href)').getall()
        for href in pages:
            url = "https://www.isna.ir" + href
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
            url = "https://www.isna.ir" + next
            if self.allowed_domains[0] in url:
                yield scrapy.Request(
                    url,
                    callback=self.parse_main,
                    errback=self.errback,
                    priority = 4
                )
'''