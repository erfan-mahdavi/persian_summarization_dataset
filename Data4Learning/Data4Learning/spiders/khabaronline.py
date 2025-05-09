import scrapy
from items import NewsItem
from spiders.base_spider import BaseSpider

class KhabaronlineSpider(BaseSpider):
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'CONCURRENT_REQUESTS_PER_DOMAIN': 16,
    }
    name = 'khabaronline'
    allowed_domains = ['khabaronline.ir']
    start_urls = ['https://www.khabaronline.ir/archive']
    

    def start_requests(self):
        
        for year in range(1394, 1405):
            for month in range(1, 13):
                for day in range(1,32):
                    url = (f"https://www.khabaronline.ir/archive?pi=1&ms=0&dy={day}&mn={month}&yr={year}")
                    yield scrapy.Request(
                        url,
                        callback=self.parse_archive,
                        errback=self.errback,
                        priority=10,
                        meta={"year": year, "month": month,"day": day, "page": 1}
                    )

    def parse_archive(self, response):
        year = response.meta["year"]
        month = response.meta["month"]
        day = response.meta["day"]
        page = response.meta["page"]

        links = response.css('li.News div.desc a::attr(href)').getall() 
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
            f"https://www.khabaronline.ir/archive?pi={next_page}&ms=0&dy={day}&mn={month}&yr={year}"
        )
        if next_page<=100:
            yield scrapy.Request(
                next_url,
                callback=self.parse_archive,
                errback=self.errback,
                priority=4,
                meta={"year": year, "month": month,"day":day, "page": next_page}
        )

    def parse_article(self, response):
        title = self.clean_text(response.css('h1.title > a::text').get())
        category = self.clean_text(response.css('li.breadcrumb-item.active > a::text').get())
        raw_nodes = response.css('div.item-text[itemprop="articleBody"] *::text').getall()
        cleaned = self.clean_nodes(raw_nodes)
        summary = self.clean_text(response.css('p.summary::text').get())

        # only yield if we have enough content:
        if title and category and len(cleaned) > 10:
            yield NewsItem(
                title=title,
                article=cleaned,
                summary=summary,
                category=category,
                tags=self.clean_tags(response.css('section.box.tags ul li a::text').getall()),
                network=self.name,
                link=response.url
            )
        '''
        for href in response.css('a::attr(href)').getall():
            url = response.urljoin(href)
            if self.allowed_domains[0] in url:
                yield scrapy.Request(url, callback=self.parse_article, errback=self.errback)
                
        def parse_main(self, response):
        for href in response.css('li.News div.desc a::attr(href)').getall():
            url = "https://www.khabaronline.ir" + href
            if self.allowed_domains[0] in url:
                yield scrapy.Request(url, callback=self.parse_article, errback=self.errback,priority=5)
        
        navs = response.css('ul.pagination li.page-item a::attr(href)').getall()
        if navs:
            nav = navs[-1]
            url = "https://www.khabaronline.ir" + nav
            if self.allowed_domains[0] in url:
                yield scrapy.Request(url, callback=self.parse_main, errback=self.errback,priority=4)
       '''