import scrapy


class BookScraperItem(scrapy.Item):
    name = scrapy.Field()
    author = scrapy.Field()
    ranking = scrapy.Field()
    genre = scrapy.Field()
    description = scrapy.Field()
