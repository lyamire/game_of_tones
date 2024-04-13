from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    username = forms.CharField(
        label='Name',
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'username', 'placeholder': 'Username', 'autocomplete': 'login', 'autofocus': True
            }),
    )
    first_name = forms.CharField(
        label='First Name',
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'first_name', 'placeholder': 'First Name'
            }),
    )
    last_name = forms.CharField(
        label='Last Name',
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'last_name', 'placeholder': 'Last Name'
            }),
    )
    email = forms.EmailField(
        required=True,
        min_length=5,
        widget=forms.EmailInput(
            attrs={
                'class': 'email', 'placeholder': 'some@email', 'autocomplete': 'email'
            }),
    )
    password1 = forms.CharField(
        label='Password',
        required=True,
        min_length=8,
        widget=forms.PasswordInput(
            attrs={
                'class': 'password', 'placeholder': 'Password', 'autocomplete': 'password'
            }),
    )
    password2 = forms.CharField(
        label='Password confirmation',
        required=True,
        min_length=8,
        widget=forms.PasswordInput(
            attrs={
                'class': 'password', 'placeholder': 'Password', 'autocomplete': 'password'
            }),
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
