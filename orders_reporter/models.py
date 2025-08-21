#loading db.models
from django.db import models
from django.contrib.auth.models import User

class Manufacturer(models.Model):
    """Manufacturer model for products details"""
    low_stock_threshold = models.IntegerField(default=5)

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.CharField(max_length=50)
    #product_img = models.ImageField(upload_to="images/", required=False)
    quantity = models.IntegerField()
    date_of_production = models.DateTimeField()
    sku = models.CharField(max_length=50, unique=True)
    date_added = models.DateTimeField(auto_now=True)
    location = models.CharField(max_length=50)


class Note(models.Model):
    """Note Model for feedback functionality"""
    name = models.CharField(max_length=50)
    feedback = models.TextField(max_length=600)


class SearchProduct(models.Model):
    """Seach product model for retrieve information"""
    query = models.CharField(max_length=100)

class Coach(models.Model):
    coach_number = models.CharField(max_length=20)
    departure_location = models.CharField(max_length=100)
    arrival_location = models.CharField(max_length=100)
    seat_capacity = models.IntegerField()

    def __str__(self):
        return self.coach_number