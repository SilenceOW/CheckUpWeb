from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import *


admin.site.register(Group)
admin.site.register(UserStatuses)
admin.site.register(File)
admin.site.register(Work)
admin.site.register(WorkType)


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profiles'


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)