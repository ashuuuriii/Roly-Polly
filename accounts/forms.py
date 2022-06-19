from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=32, label="First Name", required=False)
    last_name = forms.CharField(max_length=32, label="Last Name", required=False)

    class Meta:
        model = CustomUser
        # adding first_name and last_name here will cause them to saved twice to 2 different users
        fields = ("username", "email")

    def signup(self, request, user):
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.save()
        return user


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email")
