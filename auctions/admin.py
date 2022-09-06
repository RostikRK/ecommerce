from django.contrib import admin
from .models import User, Auction_listing, Bid, Comment, Category, Watchlist

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'is_active', 'date_joined')
    search_fields = ['first_name', 'last_name', 'date_joined']

@admin.register(Auction_listing)
class AuctionAdmin(admin.ModelAdmin):
    list_display = ('title', 'current_bid', 'date_created')
    search_fields = ['title','date_created']

@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_created')
    search_fields = ['user', 'date_created']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_created')
    search_fields = ['user', 'date_created']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name',]

@admin.register(Watchlist)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('user',)