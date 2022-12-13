import scrapy
from book_scraper.book_scraper.items import BookScraperItem

#queries = ["рассказы", "фэнтези"]


class KnigopoiskSpider(scrapy.spiders):
    name = 'knigopoisk'
    allowed_domains = ['knigopoisk.org']
    start_urls = ['https://knigopoisk.org/search/fastsearch?q=']
    url_base = 'https://knigopoisk.org'

    def start_requests(self):
        for query in queries:
            search_url = self.start_urls[0] + query
            yield scrapy.Request(url=search_url, callback=self.parse)

    def parse(self, response):
        for book_link in response.xpath('//div[@class="main-list-item-right-1 block-table"]//a/@href').extract():
            if book_link[:5] == 'https' and 'author' not in book_link:
                yield scrapy.Request(url=book_link, callback=self.parse_book)

    def parse_book(self, response):
        item = BookScraperItem()
        item['name'] = response.css('h1.page__title::text').get().split(' - ')[1]
        item['author'] = response.css('h1.page__title::text').get().split(' - ')[0]
        item['ranking'] = response.css('span.rating::text').get()
        try:
            item["genre"] = response.xpath('//table[@class="short-info"]//span//text()').extract()[0]
        except:
            item["genre"] = ' '
        item['description'] = response.xpath('//div[@id="description-block"]//text()').extract()[0]
        yield item
