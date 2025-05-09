import scrapy
from items import NewsItem

class BaseSpider(scrapy.Spider):
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                callback=self.parse_main,
                errback=self.errback,
                dont_filter=True
            )


    def errback(self, failure):
        self.logger.error(f"Request failed: {failure.request.url} – {failure.value}")

    def parse_main(self, response):
        raise NotImplementedError('Override in subclass')

    def clean_nodes(self, text_nodes):
        cleaned = []
        if not text_nodes:
            return ''
        for t in text_nodes:
            t = t.replace("\n", "")
            t = t.replace("\t", "")
            t = t.replace("\\", "")
            t = t.replace("/", "") 
            txt = t.strip()
            if not txt or txt.isdigit():
                continue
            '''
            if any(phrase in txt for phrase in bp):
                continue
            '''
            cleaned.append(txt)
        if cleaned:
            article = ' '.join(cleaned)
            article = article.replace("\n", "")
            if article[-30:].find("انتهای پیام") != -1:  
                article = article[:article.rfind("انتهای پیام")] 

        else:
            article = ''
        article = article.strip()
        return article
    
    def clean_tags(self,text_nodes):
        cleaned = []
        for t in text_nodes:
            t = t.replace("\n", "")
            t = t.replace("\t", "")
            t = t.replace("\\", "")
            t = t.replace("/", "")                      
            t = t.strip()
            if not t or t.isdigit():
                continue
            cleaned.append(t)
        if cleaned:
            tags = ','.join(cleaned)
        else:
            tags=''
        return tags
    
    def clean_text(self,cleaned):
        if cleaned:
            cleaned = cleaned.replace("\n", "")
            cleaned = cleaned.replace("\t", "")
            cleaned = cleaned.replace("\\", "")
            cleaned = cleaned.replace("/", "")                      
            cleaned = cleaned.strip()
        else:
            cleaned=''
        return cleaned
