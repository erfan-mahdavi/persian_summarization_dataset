import scrapy, re
from items import NewsItem
from spiders.base_spider import BaseSpider

class TasnimnewsSpider(BaseSpider):
    name = 'tasnimnews'
    allowed_domains = ['tasnimnews.com']
    start_urls = ['https://www.tasnimnews.com/fa/archive']

    def start_requests(self):
        
        for year in range(1394, 1405):
            for month in range(1, 13):
                for day in range(1,32):
                    url = (f"https://www.tasnimnews.com/fa/archive?date={year}%2F{month}%2F{day}&sub=-1&service=-1&page=1")
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

        links = response.css('section.news-container article.list-item a::attr(href)').getall() 
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
            f"https://www.tasnimnews.com/fa/archive?date={year}%2F{month}%2F{day}&sub=-1&service=-1&page={next_page}"
        )
        if next_page<=40:
            yield scrapy.Request(
                next_url,
                callback=self.parse_archive,
                errback=self.errback,
                priority=4,
                meta={"year": year, "month": month,"day":day, "page": next_page}
        )

    def parse_article(self, response):
        title = self.clean_text(response.css('h1.title::text').get()) or ''
        category = response.css('ul.list-inline.details li.service a::text').getall()[-1].strip()\
                   if response.css('ul.list-inline.details li.service a') else ''
        tags = self.clean_tags(response.css('section.body section.news-container.keywords-box li.skeyword-item a::text').getall())

        raw_paragraphs = response.css('div.story p ::text').getall()
        cleaned = self.clean_nodes(raw_paragraphs)

        if title and len(cleaned)>10 and category:
            item = NewsItem(
                title=title,
                article=cleaned,
                summary=self.clean_text(response.css('h3.lead ::text').get()),
                category=category,
                tags=tags,
                network=self.name,
                link=response.url
            )
            yield item

        '''
        pre_links = response.css('a::attr(href)').getall()
        
        pre1_links = response.css('article.box-item a::attr(href)').getall()
        pre2_links = response.css('article.list-item.service-item.service-bulleted a::attr(href)').getall()
        pre3_links = response.css('article.list-item.service-item.service-first a::attr(href)').getall()
        nav_links = response.css('div.menu-container.hidden-xs li ul.sub-services li a::attr(href)').getall()
        
        nav_links = response.css('div.menu-container.hidden-xs li ul.sub-services li a::attr(href)').getall()
        
        for link_href in pre_links:
            if link_href in nav_links:
                full_url = response.urljoin(link_href)
                if full_url.startswith(('http://', 'https://')) and self.allowed_domains[0] in full_url:
                    yield scrapy.Request(full_url, callback=self.parse_article, errback=self.errback,priority=6)
            else:
                full_url = response.urljoin(link_href)
                if full_url.startswith(('http://', 'https://')) and self.allowed_domains[0] in full_url:
                    yield scrapy.Request(full_url, callback=self.parse_article, errback=self.errback,priority = 3)
        '''

'''
# now spider-specific boilerplate:
    extra_boilerplate = [
        'تمامی حقوق این سایت برای تنسیم‌نیوز محفوظ است',"انتهای پیام",'Copyright','نقل مطالب با ذکر منبع بلامانع است']

    def parse_main(self, response):
        for href in response.css('div.menu-container.hidden-xs ul.sub-services a::attr(href)').getall():
            url = response.urljoin(href)
            if self.allowed_domains[0] in url:
                yield scrapy.Request(
                    url,
                    callback=self.parse_article,
                    errback=self.errback
'''