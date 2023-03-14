from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_listing", views.new_listing, name="new_listing"),
    path("auctions/<str:id>", views.listing, name="listing"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category>", views.category, name="category"),
    path("watchlist/<str:user_id>", views.watchlist, name="watchlist"),
    path("add_watch/<str:listing_id>", views.add_watch, name="add_watch"),
    path("remove_watch/<str:listing_id>", views.remove_watch, name="remove_watch"),
    path("new_bid/<str:listing_id>", views.new_bid, name="new_bid")
]
