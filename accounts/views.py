from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import CreateUserForm, UserProfileForm


def sign_up_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            profile_form = UserProfileForm(request.POST)
            if form.is_valid() and profile_form.is_valid():
                user = form.save()

                profile = profile_form.save(commit=False)
                profile.user = user

                profile.save()

                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect('/')
        else:
            form = CreateUserForm()
            profile_form = UserProfileForm()

        context = {'form': form, 'profile_form': profile_form}
        return render(request, 'accounts/signup.html', context)


def login_page(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.info(request, 'Имя пользователя ИЛИ пароль неправильные')

        context = {}
        return render(request, 'accounts/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('login')
