import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from database_creator_scrapy.database_creator_scrapy.items import ScrapyAllBooksItem

class LivelibSpider(CrawlSpider):
    name = 'livelib'
    allowed_domains = ['www.livelib.ru']
    start_urls = ['http://www.livelib.ru/']

    rules = (
        Rule(LinkExtractor(allow=r'https://www.livelib.ru/book/'), callback='parse', follow=True),
    )

    def parse(self, response):
        item = ScrapyAllBooksItem()
        item['name'] = response.css('h1.bc__book-title::text').get()
        item['author'] = response.css('a.bc-author__link::text').get()
        try:
            ranking = float(response.css('a.bc-rating-medium').attrib['title'].split(' ')[1])
            item['ranking'] = ranking
        except:
            item['ranking'] = 0
        try:
            genre = (response.xpath('//a[@class=""]/text()').extract())[0]
            genre = genre.split('\xa0')
            item["genre"] = genre[-1]
        except:
            item["genre"] = "Unknown"
        try:
            item['description'] = response.css('div[id="lenta-card__text-edition-escaped"]').get().split('\n')[1].strip()
        except:
            item['description'] = ''
        yield item
