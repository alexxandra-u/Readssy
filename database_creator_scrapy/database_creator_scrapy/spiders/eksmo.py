import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from database_creator_scrapy.database_creator_scrapy.items import ScrapyAllBooksItem

class EksmoSpider(CrawlSpider):
    name = 'eksmo'
    allowed_domains = ['eksmo.ru']
    start_urls = ['http://eksmo.ru/']

    rules = (
        Rule(LinkExtractor(allow=r'https://eksmo.ru/book/'), callback='parse', follow=True),
    )


    def parse(self, response):
        item = ScrapyAllBooksItem()
        item['name'] = response.css('h1.book-page__card-title::text').extract()[0]
        try:
            item['author'] = response.xpath('//div[@class="book-page__card-author"]//text()').extract()[0]
        except:
            item["author"] = ' '
        # item['ranking'] = response.xpath('')
        # item["genre"] =
        item['description'] = ''.join(response.xpath(
            '//div[@class="spoiler__text t t_last-p-no-offset book-page__card-description-text"]//text()').extract())
        yield item
