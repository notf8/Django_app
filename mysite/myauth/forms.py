from django import forms
from django.contrib.auth.models import User
from django.views.generic.edit import FormMixin

from .models import Profile


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "email", "first_name", "last_name",


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "agreement_accepted", "bio", "avatar"

    # email = forms.CharField()
    # first_name = forms.CharField()
    # last_name = forms.CharField()


