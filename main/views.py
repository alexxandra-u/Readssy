from django.http import HttpResponse
from django.shortcuts import render, redirect
import re
import json
from .models import Book, ReadList
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required

# from scrapy.crawler import CrawlerProcess, CrawlerRunner

prepositions = ["в", "без", "до", "из", "к", "на", "по", "о", "от", "перед", "при", "через", "для", "с", "у", "за",
                "над", "об", "под", "про"]


def search_books(request):
    print(request.method)
    print(request.POST)
    if request.method == "GET" and 'q' in request.GET and request.GET['q']:
        q = request.GET['q'].strip()
        queries = re.sub(' +', ' ', q.strip().lower()).split(' ')  # какие слова будем искать в названии книжки
        queries = [i for i in queries if i not in prepositions]  # убираем предлоги
        suitable = []  # вот сюда пока сохраню подошедшие книги
        with open('main/items.json') as json_file:
            data = json.load(json_file)
            cnt = 0
            for i in range(10346):
                for query in queries:
                    if (data[i]["name"] and query in data[i]["name"]) or (
                            data[i]["genre"] and query in data[i]["genre"]) or (
                            data[i]["description"] and query in data[i]["description"]):
                        try:
                            convert_to_empty(data[i])
                            book = Book.objects.get(description=data[i]["description"], name=data[i]["name"],
                                                    author=data[i]["author"])
                        except:
                            book = Book(name=data[i]["name"], author=data[i]["author"], ranking=data[i]["ranking"],
                                        genre=data[i]["genre"], description=data[i]["description"])
                            book.save()
                        data[i]["id"] = book.id
                        suitable.append(data[i])
                        cnt += 1
                if cnt > 20:
                    break
        return render(request, 'main/books_list.html', {'books': suitable, "query": q})

    if request.method == "POST":
        p = request.POST
        user = request.user
        if not user.is_authenticated:
            return render(request, 'main/home.html')
        if 'create_readlist' in p:
            print('yep')
            readlist = user.readlist_set.create()
            readlist.title = p.get('readlist_title', 'Новый ридлист')
            for el in p:
                if el.startswith('add-to-readlist-'):
                    book = Book.objects.get(id=el.split('add-to-readlist-')[-1])
                    print(book.name)
                    readlist.books.add(book)
            readlist.save()
    return redirect('home')


@login_required(login_url="login")
def lists_view(request):
    if request.method == "POST":
        for el in request.POST:
            if el.startswith('delete-readlist-'):
                ReadList.objects.get(id=el.split('delete-readlist-')[-1]).delete()

    readlists = ReadList.objects.filter(user=request.user)
    return render(request, "main/display_readlists.html", {"lists": readlists})


@login_required(login_url="login")
def readlist_view(request, id):
    print('here')
    if request.method == "POST":
        readlist = ReadList.objects.get(id=id)
        for el in request.POST:
            if el.startswith('delete-book-from-readlist-'):
                print('deleting')
                book = Book.objects.get(id=el.split('delete-book-from-readlist-')[-1])
                readlist.books.remove(book)
            readlist.save()
    readlist = ReadList.objects.get(id=id)
    return render(request, "main/display_readlist.html", {"list": readlist})


def convert_to_empty(data):
    data["name"] = (data["name"] if data["name"] is not None else "")
    data["author"] = (data["author"] if data["author"] is not None else "")
    data["genre"] = (data["genre"] if data["genre"] is not None else "")
    data["description"] = (data["description"] if data["description"] is not None else "")
    data["ranking"] = (data["ranking"] if data["ranking"] is not None else 0.0)


def home_view(request):
    return render(request, 'main/home.html')
