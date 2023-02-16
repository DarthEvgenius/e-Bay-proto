from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Categories(models.Model):
    category = models.CharField(max_length=20)

class Listings(models.Model):
    title = models.CharField(max_length=50)
    # Who is owner of the listing
    # We can look for this user's other listings
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_listings")
    init_price = models.IntegerField()
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name="category_listings")
    # If the listing is active or not
    status = models.BooleanField()
    image = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)

