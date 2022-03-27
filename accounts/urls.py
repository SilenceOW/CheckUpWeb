from django.urls import path, include
from . import views


urlpatterns = [
    path('login', views.login_page, name="login"),
    path('signup', views.sign_up_page, name="signup"),
    path('logout', views.logout_user, name="logout"),
]
