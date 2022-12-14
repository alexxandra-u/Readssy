import scrapy
from book_scraper.book_scraper.items import BookScraperItem

#queries = ["рассказы", "фэнтези"]

class LivelibSpider(scrapy.Spider):
    name = 'livelib'
    allowed_domains = ['www.livelib.ru']
    start_urls = ['https://www.livelib.ru/find/books/']
    url_base = 'https://www.livelib.ru'

    def start_requests(self):
        for query in queries:
            search_url = self.start_urls[0] + query
            yield scrapy.Request(url=search_url, callback=self.parse)

    def parse(self, response):
        cur_link = str(response).split(' ')[1][:-1]
        number_of_books_found = int(response.xpath('//li[@class="active"]//b//text()').extract()[0])
        number_of_pages = number_of_books_found//20
        for page_num in range(1, number_of_pages):
            page_link = cur_link + '/~' + str(page_num)
            yield scrapy.Request(url=page_link, callback=self.parse_page)

    def parse_page(self, response):
        for book_link in response.xpath('//div[@class="object-wrapper object-edition ll-redirect-book"]//a/@href').extract()[::2]:
             if book_link[:5] == '/book' and 'editions' not in book_link:
                total_link = self.url_base + book_link
                yield scrapy.Request(url=total_link, callback=self.parse_book)

    def parse_book(self, response):
        item = BookScraperItem()
        item['name'] = response.css('h1.bc__book-title::text').get()
        item['author'] = response.css('a.bc-author__link::text').get()
        try:
            ranking = response.css('a.bc-rating-medium').attrib['title'].split(' ')[1]
            if isinstance(ranking, int):
                item['ranking'] = ranking
            else:
                item['ranking'] = 0
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

