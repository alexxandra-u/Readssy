from django.db import models

# Create your models here.

class Book(models.Model):
    name = models.TextField(default=' ')
    author = models.TextField(default=' ')
    ranking = models.FloatField(default=0.0)
    genre = models.TextField(default=' ')
    description = models.TextField(default=' ')