from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    name = models.TextField(default=' ')
    author = models.TextField(default=' ')
    ranking = models.FloatField(default=0.0)
    genre = models.TextField(default=' ')
    description = models.TextField(default=' ')


class ReadList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=300, default="Новый ридлист")
    description = models.TextField(default=" ")
    books = models.ManyToManyField(Book)
