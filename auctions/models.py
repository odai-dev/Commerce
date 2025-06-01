from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    CATEGORY_CHOICES = [
        ("electronics", "Electronics"),
        ("fashion", "Fashion & Accessories"),
        ("home", "Home & Kitchen"),
        ("sports", "Sports & Outdoors"),
        ("beauty", "Beauty & Personal Care"),
        ("books", "Books & Magazines"),
        ("toys", "Toys & Games"),
        ("phones", "Smartphones"),
        ("computers", "Computers & Laptops"),
        ("gaming", "Gaming & Consoles"),
        ("cars", "Cars"),
        ("rent", "Apartments for Rent"),
        ("freelance", "Freelancing Services"),
        ("collectibles", "Collectibles"),
        ("misc", "Miscellaneous"),
    ]
    title = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_highest_bid = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    category = models.CharField(max_length=64, choices=CATEGORY_CHOICES, blank=True)
    image_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    time_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} (${self.starting_price}) url: {self.image_url}"


class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    bid_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bidder.username} - ${self.amount} on {self.listing.title}"


class Comment(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.commenter.username} on {self.listing.title}"
