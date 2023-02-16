from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    category = models.CharField(max_length=20)

class Listing(models.Model):
    title = models.CharField(max_length=50)
    # Who is owner of the listing
    # We can look for this user's other listings
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_listings")
    init_price = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category_listings")
    # If the listing is active or not
    status = models.BooleanField()
    image = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)

class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=1000)

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.IntegerField()
    time = models.DateTimeField(auto_now=True)

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_watchlist")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)