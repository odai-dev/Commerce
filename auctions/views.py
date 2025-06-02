from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from decimal import Decimal

from .models import User, Listing, Comment, Bid
from .forms import ListingForm

@login_required
def index(request):
    listings = Listing.objects.filter(is_active=True)
    return render(request, "auctions/index.html", {
        "listings": listings
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

@login_required
def new_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.save()
            return redirect("index")
    else:
        form = ListingForm()
    return render(request, "auctions/new_listing.html", {
        "form": form
    })

@login_required
def listing_detail(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    comments = listing.comments.all()
    bids = listing.bids.all()
    is_owner = request.user == listing.owner

    current_bid = listing.current_highest_bid or listing.starting_price
    winner = None 
    if not listing.is_active:
        if bids.exists():
            winner = bids.latest('amount').bidder

    return render(request, "auctions/listing_detail.html", {
        "listing": listing,
        "comments": comments,
        "is_owner": is_owner,
        "current_bid": current_bid,
        "winner": winner
    })

@login_required 
def place_bid(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)

    if request.method == "POST":
        try:
            bid_amount = Decimal(request.POST["bid_amount"].strip())
        except:
            messages.error(request, "Invalid bid amount.")
            return redirect("listing_detail", listing_id=listing_id)
        
        current_price = listing.current_highest_bid or listing.starting_price

        if bid_amount <= current_price:
            messages.error(request, "Your bid must be higher than the current price.")
            return redirect(listing_detail, listing_id=listing_id)
    
        bid  = Bid (bidder=request.user, listing=listing, amount=bid_amount)
        bid.save()

        listing.current_highest_bid = bid_amount
        listing.save()

        messages.success(request, "Your bid was placed successfully")
        return redirect("listing_detail", listing_id=listing_id)
    return redirect("listing_detail", listing_id=listing_id)

@login_required
def close_listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)

    if request.method == "POST":
        if request.user != listing.owner:
            messages.error(request, "Only the listing owner can close the listing.")
            return redirect("listing_detail", listing_id=listing_id)

        listing.is_active = False 
        listing.save()
        messages.success(request, "Listing closed successfully.")
        return redirect("index")

    return redirect("listing_detail", listing_id=listing_id)

@login_required
def add_comment(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)

    if request.method == "POST":
        content = request.POST["content"].strip()
        if not content:
            messages.error(request, "Please write a comment before submiting")
            return redirect("listing_detail", listing_id=listing_id)

        comment = Comment( commenter = request.user, listing=listing, content=content)
        comment.save()

        messages.success(request, "Comment added successfully.")
        return redirect("listing_detail", listing_id=listing_id)
    
    return redirect("listing_detail", listing_id=listing_id)
