from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from main.models import Profile


class CreateUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    error_messages = {
        'password_mismatch': "Пароли не совпадают",
    }

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        help_texts = {
            'email': 'Введите ваш настоящий адрес электронной почты',
            'password': 'Ваш пароль должен состоять как минимум из 8 символов и быть набором букв и цифр',
            'password2': 'пароли не совпадают',
            'username': 'Имя пользователя должно состоять из букв и цифр'
        }


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={
                'class': 'form-control',
                'required': 'true',
            })
        }
