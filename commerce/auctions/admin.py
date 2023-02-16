from django.contrib import admin
# admin usernamme = admin, pass = 0000

from .models import User, Category, Listing, Comment, Bid, Watchlist

# Register your models here.

# View style in admin-app
class UserAdmin(admin.ModelAdmin):
	list_display = ("id", "username", "first_name", "last_name", "email")

admin.site.register(User, UserAdmin)
admin.site.register(Category)
admin.site.register(Listing)
admin.site.register(Comment)
admin.site.register(Bid)
admin.site.register(Watchlist)
