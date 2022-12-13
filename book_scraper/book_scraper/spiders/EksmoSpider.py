import scrapy
from book_scraper.book_scraper.items import BookScraperItem

#queries = ["рассказы", "фэнтези"]

class EksmoSpider(scrapy.spiders):
    name = 'eksmo'
    allowed_domains = ['eksmo.ru']
    start_urls = ['https://eksmo.ru/search/?q=']
    url_base = 'https://eksmo.ru'

    def start_requests(self):
        for query in queries:
            search_url = self.start_urls[0] + query
            yield scrapy.Request(url=search_url, callback=self.parse)

    def parse(self, response):
        for book_link in response.xpath('//div[@class="book__link"]//a/@href').extract():
             if book_link[:5] == '/book':
                total_link = self.url_base + book_link
                yield scrapy.Request(url=total_link, callback=self.parse_book)

    def parse_book(self, response):
        item = BookScraperItem()
        item['name'] = response.css('h1.book-page__card-title::text').extract()[0]
        try:
            item['author'] = response.xpath('//div[@class="book-page__card-author"]//text()').extract()[0]
        except:
            item["author"] = ' '
        item['description'] = ''.join(response.xpath('//div[@class="spoiler__text t t_last-p-no-offset book-page__card-description-text"]//text()').extract())
        yield item
