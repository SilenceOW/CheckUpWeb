from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.works_teacher, name='works'),
    path('add', views.add_work, name='add_work'),
    path('check/<int:work_id>/<int:file_id>', views.check_work, name='check_work'),
    path('add/<int:work_id>', views.add_file, name='add_file')
]