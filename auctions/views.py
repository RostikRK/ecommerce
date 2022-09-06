from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from datetime import datetime
from auctions.forms import UserImage
from django.conf import settings

from .models import User, Auction_listing, Category, Auction_image, Watchlist, Bid, Comment


def index(request):
    if request.user.is_authenticated:
        context = {"listings": Auction_listing.objects.filter(active=True), "watchlist": Watchlist.objects.get(user=request.user)}
        return render(request, "auctions/index.html", context)
    else:
        context = {"listings": Auction_listing.objects.filter(active=True)}
        return render(request, "auctions/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return redirect("auctions:index")
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

@login_required(login_url="auctions:login")
def logout_view(request):
    logout(request)
    return redirect("auctions:index")


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        birthday = request.POST["birthday"]
        phonenum = request.POST["telNo"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password, phonenum=phonenum, birthday=birthday)
            user.save()
            Watchlist.objects.create(user=user)
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return redirect("auctions:index")
    else:
        return render(request, "auctions/register.html")

@login_required(login_url="auctions:login")
def create(request):
    context = {"categories": Category.objects.all(), 'form': UserImage()}
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        st_bid = request.POST["bid"]
        creator = request.user
        category = [Category.objects.get(name=request.POST["category"])]
        form = UserImage(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data.get("image")
        try:
            auction_image = Auction_image(image=image)
            auction_image.save()
            print("______________________________")
            auction = Auction_listing.objects.create(creator=creator, title=title, description=description, start_bid=st_bid, current_bid=st_bid, image_obj=auction_image)
            print("______________________________")
            auction.category.set(category)
            print("______________________________")
            auction.save()
        except IntegrityError:
            context["message"] = "Auction already taken"
            return render(request, "auctions/create.html", context)
        return redirect("auctions:index")
    else:
        return render(request, "auctions/create.html", context)

@login_required(login_url="auctions:login")
def add_to_wishlist(request, auction_id):
    wishlist = Watchlist.objects.get(user=request.user)
    auction = get_object_or_404(Auction_listing, id=auction_id)
    print(auction)
    wishlist.auctions.add(auction)
    wishlist.in_watchlist += 1
    wishlist.save()
    return redirect("auctions:index")

@login_required(login_url="auctions:login")
def watchlist(request):
    watchlist = Watchlist.objects.get(user=request.user)
    for auction in watchlist.auctions.all():
        print(auction)
    return render(request, "auctions/wishlist.html", {"watchlist": Watchlist.objects.get(user=request.user)})

@login_required(login_url="auctions:login")
def categories(request):
    return render(request, "auctions/categories.html", {"categories": Category.objects.all()})

@login_required(login_url="auctions:login")
def categorized(request, category_id):
    if request.user.is_authenticated:
        listing = set()
        for auction in Auction_listing.objects.filter(active=True):
            for category in auction.category.all():
                if category.id == category_id:
                    listing.add(auction)
        context = {"listings": listing, "watchlist": Watchlist.objects.get(user=request.user), "category_id": category_id}
        return render(request, "auctions/categorized.html", context)
    else:
        return render(request, "auctions/categorized.html")

@login_required(login_url="auctions:login")
def listing(request, auction_id):
    auction = Auction_listing.objects.get(id=auction_id)
    return render(request, "auctions/listing.html", {"auction": auction, "bids": Bid.objects.filter(auction=auction), "comments": Comment.objects.filter(auction=auction)})