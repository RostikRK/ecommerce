from django.db import models  
from django.forms import fields  
from .models import Auction_image  
from django import forms  
  
  
class UserImage(forms.ModelForm):  
    class Meta:  
        # To specify the model to be used to create form  
        model = Auction_image  
        # It includes all the fields of model  
        fields = ['image']