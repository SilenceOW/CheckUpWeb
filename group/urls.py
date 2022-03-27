from django.contrib import admin
from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('group/<int:id>', views.group, name='group'),
    path('', views.groups, name='groups'),
    path('groups/delete/<int:pk>', views.leave_group, name='leave'),
    path('group/<int:id>/kick/<int:pk>', views.kick_user, name='kick'),
    path('group/<int:id>/works/', include('works.urls'))
]
