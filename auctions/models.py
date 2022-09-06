from django.contrib.auth.models import AbstractUser
from django.db import models
import pathlib
import uuid
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone


class User(AbstractUser):
    phonenum = PhoneNumberField(default="+", null=True, blank=True)
    birthday = models.DateTimeField(default=None, null=True, blank=True)

class Category(models.Model):
    name = models.CharField(max_length=50)
    category_image = models.ImageField(upload_to="categories_image/")

def auction_image_handler(instance, filename):
    fpath = pathlib.Path(filename)
    new_fname = str(uuid.uuid1())
    return f"auction_images/{new_fname}{fpath.suffix}"

class Auction_image(models.Model):
    image = models.ImageField(upload_to=auction_image_handler)


class Auction_listing(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator')
    title = models.CharField(max_length=150)
    description = models.TextField()
    start_bid = models.FloatField()
    current_bid = models.FloatField()
    active = models.BooleanField(default=True)
    category = models.ManyToManyField(Category)
    date_created = models.DateTimeField(default=timezone.now)
    image_obj = models.OneToOneField(Auction_image, on_delete=models.CASCADE, null=True, blank=True)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name='winner', null=True, blank=True)
    amount_of_bids = models.IntegerField(default=0)
    def get_image(self):
        return self.image_obj.image

class Bid(models.Model):
    auction = models.ForeignKey(Auction_listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bid = models.FloatField()
    date_created = models.DateTimeField(default=timezone.now)

class Comment(models.Model):
    auction = models.ForeignKey(Auction_listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)

class Watchlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    auctions = models.ManyToManyField(Auction_listing, null=True, blank=True)
    in_watchlist = models.IntegerField(default=0)