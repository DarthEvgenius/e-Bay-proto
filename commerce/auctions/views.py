from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm, Textarea

from .models import User, Listing, Category


# Form class for a new listing
class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'category', 'init_price', 'image', 'description']
        widgets = {
            'description': Textarea(attrs={'cols': 80, 'rows': 10})
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

            # Fill the missing field ("status" field has defaut, and "winner" will be set when the listing will be closed)
            seller = request.user.username
            listing.seller = User.objects.get(username=seller)

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

    # Pass the listing to the template
    return render(request, "auctions/listing.html", {
        "listing": listing
    })


def categories(request):
    """ Shows the list of caegories """
    
    categories = Category.objects.all()

    return render(request, "auctions/categories.html", {
        "categories": categories
    })


def category(request, category):
    """ Shows all the active listings of that category """

    # Get id of the category, because Foreign Key wants id of the Primary key
    cat_id = Category.objects.get(category=category)
    
    # Get listings
    category_listings = Listing.objects.filter(category=cat_id)

    print(category_listings)

    # Get all the categories to view them
    categories = Category.objects.all()

    return render(request, "auctions/categories.html", {
        "category_listings": category_listings,
        "categories": categories
    })