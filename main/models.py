from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, m2m_changed, post_save
from django.dispatch import receiver
from django.shortcuts import reverse
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist
from django.core.signals import request_finished
import datetime

# constants
DEFAULT_STATUS_ID = 1


class UserStatuses(models.Model):
    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title


class Group (models.Model):
    title = models.CharField(max_length=100)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('group', kwargs={'id': self.id})

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(null=True, blank=True)
    groups = models.ManyToManyField(Group, blank=True)
    status = models.ForeignKey(UserStatuses, on_delete=models.PROTECT, default=DEFAULT_STATUS_ID)

    def __str__(self):
        return f'{self.user.username}'


# Если создатель выходит из группы/удаляет группу, то группа удаляется
# @receiver(signal=m2m_changed, sender=Profile.groups.through)
# def delete_group(instance, action, pk_set, model, **kwargs):
#     if action == 'post_remove':
#         if model != Group:
#             return
#         _group = model.objects.get(id=pk_set.pop())
#         if _group.creator == instance.user:
#             _group.delete()


# Добавляет создателя в группу
@receiver(post_save, sender=Group)
def add_creator_to_group(instance, created, **kwargs):
    print(instance)
    if created:
        _creator = instance.creator
        instance.profile_set.add(_creator.profile)


class WorkType(models.Model):
    Title = models.CharField(max_length=50)

    def __str__(self):
        return self.Title


def user_directory_path(instance, filename):
    return f'user/{instance.user.username}/{datetime.datetime.now().strftime("%Y-%m-%d")}/{filename}'


# Информация о работе (До какого времени сделать, тип работы, в какой группе, кто выложил)
class Work(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    toDate = models.DateTimeField(null=True)
    subject = models.CharField(max_length=50)
    Title = models.ForeignKey(WorkType, on_delete=models.SET_NULL, null=True)
    in_group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    work_file = models.FileField(upload_to=user_directory_path)

    def __str__(self):
        return f'{self.in_group} | {self.Title} | {self.id}'


# Отправленный файл/работа ученика. Статус (1 - отправлена, на проверке, 2 - проверена, есть оценка)
class File(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    work = models.ForeignKey(Work, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mark = models.IntegerField(blank=True, null=True)
    file = models.FileField(upload_to=user_directory_path)
    teach_ans = models.FileField(upload_to=user_directory_path, blank=True)

    def __str__(self):
        return f'{self.user} | {self.work} | {self.date}'
