# imports 
from dataclasses import fields
from django.forms import ModelForm
from .models import Room

# Form Calculations 
class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
