from django.shortcuts import render
import re
import json
#from scrapy.crawler import CrawlerProcess, CrawlerRunner

prepositions = ["в", "без", "до", "из", "к", "на", "по", "о", "от", "перед", "при", "через", "для", "с", "у", "за",
                "над", "об", "под", "про"]

def home_view(request):
    if request.method == 'POST':
        p = request.POST
        queries = re.sub(' +', ' ', p['s'].strip().lower()).split(' ')   # какие слова будем искать в названии книжки
        queries = [i for i in queries if i not in prepositions]  # убираем предлоги
        suitable  = []  #вот сюда пока сохраню подошедшие книги
        with open('main/items.json') as json_file:
            data = json.load(json_file)
            cnt = 0
            for i in range(10346):
                for query in queries:
                    if (data[i]["name"] and query in data[i]["name"]) or (data[i]["genre"] and query in data[i]["genre"]) or (data[i]["description"] and query in data[i]["description"]):
                        suitable.append(data[i])
                        print(data[i]["name"])
                        cnt += 1
                if cnt > 20:
                    break

        # ПОПЫТКА ВЫЗВАТЬ SCRAPY ЧЕРЕЗ CRAWLPROCESS (кажется вот это должно быть правильным вариантом)
        # process = CrawlerProcess()
        # process.crawl(LivelibSpider)
        # process.start()

        # ПОПЫТКА ВЫЗВАТЬ SCRAPY ЧЕРЕЗ CRAWLRUNNER
        # runner = CrawlerRunner()
        # runner.crawl(LivelibSpider.LivelibSpider)
        # runner.crawl(EksmoSpider.EksmoSpider)
        # runner.crawl(KnigopoiskSpider.KnigopoiskSpider)
        # reactor.run()
        # print("smth worked")
        # d = runner.join()
        # d.addBoth(lambda _: reactor.stop())

        # ПОПЫТКА ВЫЗВВАТЬ SCRAPY ЧЕРЕЗ CMDLINE
        # cmdline.execute(["cd","./"])
        # cmdline.execute(["scrapy", "crawl", "livelib"])
        # book_scraper.scrapy_main.run_spiders(queries)

        # ПОПЫТКА ВЫЗВАТЬ SCRAPY ЧЕРЕЗ SUBPROCESS
        # subprocess.call(["cd", ".."], shell = True)
        # subprocess.call('ls', shell=True, cwd='path/to/wanted/dir/')
        # subprocess.call(["scrapy", "crawl", 'livelib', "-o", "items.json"], cwd='./book_scraper', shell=True)
        # subprocess.call(["scrapy", "crawl", "livelib", "-o", "items.json"], cwd='~/PycharmProjects/readssy/scraper', shell=True)


    return render(request, "main/home.html")