from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm, Textarea
from django import forms

from .models import User, Listing, Category, Bid, Comment


# Form class for a new listing
class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'category', 'init_price', 'image', 'description']
        widgets = {
            'description': Textarea(attrs={'cols': 80, 'rows': 10})
        }


# Form class for a new comment
class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': Textarea(attrs={'cols': 40, 'rows': 2})
        }
        labels = {
            'content': 'Type your comment here:'
        }


def index(request):
    """ Views all of the currently active auction listings """

    # Get all active listings
    active_listings = Listing.objects.filter(status=True)
    
    # Give this Query Set to the template
    return render(request, "auctions/index.html", {
        "active_listings": active_listings
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


# Decorator makes view available for logged users only
@login_required
def new_listing(request):
    """ Creates a new listing """

    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            # We can manually get data from the Form:
            # title = form.cleaned_data['title']
            # category = form.cleaned_data['category']
            # init_price = form.cleaned_data['init_price']
            # image = form.cleaned_data['image']
            # description = form.cleaned_data['description']

            # But using method form.save() will create and save a database object automatically!
            # And form.save(commit=False) allows to set values of the missing fields in ListingForm

            # Create, but don't save the new listing instance.
            listing = form.save(commit=False)

            # Fill the missing fields ("status" field has defaut, and "winner" will be set when the listing will be closed)
            seller = request.user.username
            listing.seller = User.objects.get(username=seller)
            
            # When we create a listing init price is the current
            listing.current_price = form.cleaned_data['init_price']

            # Save the new instance.
            listing.save()

            # Now, save the many-to-many data for the form.
            form.save_m2m()


            # return render(request, "auctions/index.html", {
            #     "message": f"{seller}"
            # })
            return HttpResponseRedirect(reverse("index"))

        return render(request, "auctions/new_listing.html", {
            "form": form
        })
    else:
        return render(request, "auctions/new_listing.html", {
            "form": ListingForm()
        })


def listing(request, id):
    """ Shows the details of the listing """

    # Get the listing by id
    listing = Listing.objects.get(id=id)

    # Check if the listing is in user's watchlist (return 1/0 after query)
    inWatchlist = request.user in listing.watchlist.all()

    # Get the last bid for the listing
    # If there are no bids, current_price will be the same as the init_price
    # In that case we start bids from the current_price
    # In other cases we start from current_price + 1
    old_bid = listing.current_price
    if listing.init_price != listing.current_price:
        old_bid += 1

    # Get comments about the listing, ordering in reverse
    comments = Comment.objects.filter(listing=listing).order_by("-pk")

    # Pass the listing to the template
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "inWatchlist":inWatchlist,
        "old_bid": old_bid,
        "comments": comments,
        "commentForm": CommentForm()
    })


@login_required
def add_watch(request, listing_id):
    """ Adds the listing to the user's watchlist"""

    # Get the listing by id
    listing = Listing.objects.get(id=listing_id)

    # Get the username
    user = request.user.pk
 
    # Create the relation
    listing.watchlist.add(user)

    return HttpResponseRedirect(reverse("listing", args=(listing_id, )))


@login_required
def remove_watch(request, listing_id):
    """ Removes the listing from the user's watchlist"""

    # Get the listing by id
    listing = Listing.objects.get(id=listing_id)

    # Get the username
    user = request.user.pk
 
    # Create the relation
    listing.watchlist.remove(user)

    return HttpResponseRedirect(reverse("listing", args=(listing_id, )))



def categories(request):
    """ Shows the list of caegories """
    
    categories = Category.objects.all()

    return render(request, "auctions/categories.html", {
        "categories": categories
    })


def category(request, category):
    """ Shows all the active listings of that category """

    # Message for possibly emmpty category
    message = ""

    # Get listings
    category_listings = Listing.objects.filter(category=category)

    if not category_listings:
        message = "There are no active listings in this category"

    # Get all the categories to view them
    categories = Category.objects.all()

    return render(request, "auctions/categories.html", {
        "category_listings": category_listings,
        "categories": categories,
        "message": message
    })


@login_required
def watchlist(request, user_id):
    """ Shows the user's watchlist of listings """

    # Get the current user
    current_user = User.objects.get(pk=user_id)

    # Get all the watched listings of the user via related name
    watchlist = current_user.user_watchlist.all()
    
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist
    })


@login_required
def new_bid(request, listing_id):
    """ Creates new bid, updates the table of Bids """

    if request.method == "POST":
        # Get listing data:
        listing = Listing.objects.get(pk=listing_id)

        # Get the current price of the listing
        old_bid = listing.current_price

        # If the listing's current_price != init_price => new bid must be greater than the current price
        if listing.init_price != listing.current_price:
            old_bid += 1

        # So, the new bid must be greater than the old bid

        # Get the user's bid and check it
        nuovo_bid = request.POST["new_bid"]
        try:
            nuovo_bid = int(nuovo_bid)
        except:
            return HttpResponseRedirect(reverse("listing", args=(listing_id, )))


        # If it's correct - update the data and refresh a listing page
        if nuovo_bid > old_bid:
            updateBid = Bid(user = request.user, price = nuovo_bid, listing = listing)
            updateBid.save()
            listing.current_price = nuovo_bid
            listing.save()
            
            return HttpResponseRedirect(reverse("listing", args=(listing_id, )))

    else:
        return HttpResponseRedirect(reverse("listing", args=(listing_id, )))


@login_required
def addComment(request, listing_id):
    """ Creates a new comment to the listing"""
    
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)

        # Get user's input
        form = CommentForm(request.POST)

        if form.is_valid():
            # Create, but don't save the new listing instance.
            comment = form.save(commit=False)

            # Filling form fields
            #listing = Listing.objects.get(pk=listing_id)
            comment.listing = Listing.objects.get(pk=listing_id)

            #author = request.user
            comment.author = request.user

            # Save the new instance.
            comment.save()

            return HttpResponseRedirect(reverse("listing", args=(listing_id, )))
        
        return HttpResponseRedirect(reverse("listing", args=(listing_id, )))
        
    else:
        return HttpResponseRedirect(reverse("listing", args=(listing_id, )))
    

@login_required
def close_listing(request, listing_id):
    """ Seller can close the listing """

    # Get the listing
    listing = Listing.objects.get(pk=listing_id)

    listing.status = False

    # Get the last bid's user
    winner = Bid.objects.filter(listing=listing).order_by("-time")[0]

    # Make him a winner
    listing.winner = winner.user

    listing.save()

    return HttpResponseRedirect(reverse("listing", args=(listing_id, )))