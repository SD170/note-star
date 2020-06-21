from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import *

class UserForm(UserCreationForm):

    
    full_name = forms.CharField(max_length=100)
    # college_name = forms.ModelChoiceField(queryset=objectlist)

    class Meta:
        model = User
        fields = ('username','full_name','email','password1','password2')

