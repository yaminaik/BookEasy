from django import forms
from django.contrib.auth import login,authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Customer,Comment

class RegisterForm(UserCreationForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ['username','email','password1','password2']

class CustomerForm(forms.ModelForm):

	class Meta:
		model = Customer
		fields = ['email']

class SearchForm(forms.Form):
	query = forms.CharField(max_length=100)

class CommentForm(forms.ModelForm):
	class Meta:
		model=Comment
		fields = ['subject','comment','rate']
	
		
