from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

    def __str__(self):
        return f"ID: {self.id}; Username: {self.username}"


class Category(models.Model):
    category = models.CharField(max_length=20)

    def __str__(self):
        return f"{ self.category }"

class Listing(models.Model):
    title = models.CharField(max_length=50)

    # Who is owner of the listing
    # We can look for this user's other listings
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_listings")

    # Decimal Field can be configured with a resolution on decimal places
    init_price = models.DecimalField(max_digits=15, decimal_places=2)

    current_price = models.DecimalField(blank=True, null=True, max_digits=15, decimal_places=2)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category_listings")
    # If the listing is active or not
    status = models.BooleanField(default=True)

    image = models.CharField(max_length=100)

    description = models.CharField(max_length=1000)

    # This field we populate after smb wil win the listing, so it could be empty
    winner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"ID: {self.id}; Title: {self.title}; seller: {self.seller}; status: {self.status}; category: {self.category}"

class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=1000)

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Listing: {self.listing.title}; User: {self.user}, {self.price}$"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_watchlist")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def __str__(self):
        return f"Listing: {self.listing.title}; User: {self.user}$"