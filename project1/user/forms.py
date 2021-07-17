from django import forms
from .models import User, Carmanagement
from django.forms import ModelForm


class u_r(ModelForm):
    class Meta:
        model=User
        fields=('username','password','phone','roll','name','position')


class u_r2(ModelForm):
    class Meta:
        model=User
        fields=('password','phone','name',)


class car_management(ModelForm):
    class Meta:
        model=Carmanagement
        fields='__all__'