from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('home/', views.home_view, name='home'),
    path('search_books/', views.search_books, name="search_books"),
    path('lists', views.lists_view, name="lists"),
    path('<int:id>', views.readlist_view, name="readlist")
]