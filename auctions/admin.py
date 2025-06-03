from django.contrib import admin
from .models import Listing, Bid, Comment, User
# Register your models here.

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "starting_price", "current_highest_bid", "owner", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("title", "description", "owner__username")


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ("listing", "bidder", "amount", "bid_time")
    search_fields = ("listing__title", "bidder__username")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("listing", "commenter", "content", "time")
    search_fields = ("listing__title", "commenter__username", "content")

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "is_staff", "is_superuser")