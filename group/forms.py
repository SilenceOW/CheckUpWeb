from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ObjectDoesNotExist


class AddUserForm(forms.Form):
    username = forms.CharField(max_length=30)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            raise forms.ValidationError("Такого пользователя не существует")
        return username


class AddGroupForm(forms.Form):
    title = forms.CharField(max_length=100)

