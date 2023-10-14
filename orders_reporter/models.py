from django.db import models
import pyqrcode
# Create your models here.
from django.db import models


class Manufacturer(models.Model):
    item = models.CharField(max_length=50)
    quantity = models.IntegerField()
    date_of_production = models.DateTimeField()
    sku = models.CharField(max_length=50, unique=True)
    date_added = models.DateTimeField(auto_now=True)
    location = models.CharField(max_length=50)

class Note(models.Model):
    name = models.CharField(max_length=50)
    feedback = models.TextField(max_length=600)

class SearchProduct(models.Model):
    query = models.CharField(max_length=100)