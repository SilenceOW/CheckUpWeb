from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('groups/', include('group.urls')),
    path('', include('accounts.urls'))
]
