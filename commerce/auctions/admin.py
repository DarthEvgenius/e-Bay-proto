from django.contrib import admin
# admin usernamme = admin, pass = 0000

from .models import User, Category, Listing, Comment, Bid, Watchlist

# Register your models here.

# View style in admin-app
class UserAdmin(admin.ModelAdmin):
	list_display = ("id", "username", "first_name", "last_name", "email")

class ListingAdmin(admin.ModelAdmin):
	list_display = ("id", "title", "status", "seller", "category")

class BidAdmin(admin.ModelAdmin):
	list_display = ("listing", "user", "price", "time")

admin.site.register(User, UserAdmin)
admin.site.register(Category)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Comment)
admin.site.register(Bid, BidAdmin)
admin.site.register(Watchlist)
