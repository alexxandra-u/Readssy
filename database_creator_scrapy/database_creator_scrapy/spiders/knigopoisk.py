import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from database_creator_scrapy.database_creator_scrapy.items import ScrapyAllBooksItem

class KnigopoiskSpider(CrawlSpider):
    name = 'knigopoisk'
    allowed_domains = ['knigopoisk.org']
    start_urls = ['http://knigopoisk.org/']

    rules = (
        Rule(LinkExtractor(allow=r'https://knigopoisk.org/books'), callback='parse', follow=True),
    )


    def parse(self, response):
        item = ScrapyAllBooksItem()
        try:
            item['name'] = response.css('h1.page__title::text').get().split(' - ')[1]
        except:
            item['name'] = ' '
        try:
            item['author'] = response.css('h1.page__title::text').get().split(' - ')[0]
        except:
            item['author'] = ' '
        item['ranking'] = response.css('span.rating::text').get()
        try:
            item["genre"] = response.xpath('//table[@class="short-info"]//span//text()').extract()[0]
        except:
            item["genre"] = ' '
        try:
            item['description'] = response.xpath('//div[@id="description-block"]//text()').extract()[0]
        except:
            item['description'] = ' '
        yield item
