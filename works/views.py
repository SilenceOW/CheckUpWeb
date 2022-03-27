from django.contrib.auth.decorators import login_required
from operator import attrgetter
from django.shortcuts import render, get_object_or_404, reverse, redirect, HttpResponseRedirect
from main.models import File, Work
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.contrib import messages
from .forms import AddWork, CheckWork, AddFile


@login_required(login_url='/login')
def works_teacher(request, id):
    _user = request.user
    _group = get_object_or_404(_user.profile.groups, id=id)
    group_users = _group.profile_set.all().exclude(status=2).order_by('user__last_name')
    _works = _group.work_set.all()
    sorted_works = sorted(_works, key=attrgetter('Title.Title'))
    context = {
        "user": _user,
        "group": _group,
        "users_group": group_users,
        "works": sorted_works,
        "works_count": len(sorted_works),
    }
    return render(request, 'works/works.html', context=context)


@login_required(login_url='/login')
def add_work(request, id):
    _user = request.user
    _group = _user.profile.groups.get(id=id)
    if _user.profile.status.id < 2:
        return redirect(reverse('works', kwargs={'id': id}))
    if request.method == "POST":
        form = AddWork(request.POST, request.FILES, initial={"user": _user, "in_group": _group})
        if form.is_valid():
            form.save()
            # this_form = form.save(commit=False)
            # this_form.in_group = _group
            # this_form.user = _user
            # this_form.save()
            form_group = form.cleaned_data['in_group']
            form_title = form.cleaned_data['Title']
            form_subject = form.cleaned_data['subject']

            messages.success(request, f'{form_title} по предмету "{form_subject}" была выложена в группу {form_group}')
            return HttpResponseRedirect(reverse('works', kwargs={'id': id}))
        else:
            print(form.errors)
    else:
        form = AddWork(initial={"user": _user, "in_group": _group})
    context = {
        "user": _user,
        "group": _group,
        "form": form
    }
    return render(request, 'works/add_work.html', context=context)


@login_required(login_url='/login')
def check_work(request, id, work_id, file_id):
    _user = request.user
    if _user.profile.status.id < 2:
        raise Http404
    _group = get_object_or_404(_user.profile.groups, id=id)
    _work = get_object_or_404(_group.work_set, id=work_id)
    _file = get_object_or_404(_work.file_set, id=file_id)
    if request.method == 'POST':
        form = CheckWork(request.POST, request.FILES, instance=_file, initial={
            'user': _file.user,
            'work': _file.work
        })
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('works', kwargs={'id': id}))
    else:
        form = CheckWork(instance=_file, initial={
            'user': _file.user,
            'work': _file.work
        })
    context = {
        "user": _user,
        "group": _group,
        "form": form,
    }
    return render(request, 'works/check_work.html', context=context)


@login_required(login_url='/login')
def add_file(request, id, work_id):
    _user = request.user
    _group = get_object_or_404(_user.profile.groups, id=id)
    _work = get_object_or_404(_group.work_set, id=work_id)
    try:
        user_file = _work.file_set.get(user=_user)
        raise Http404
    except ObjectDoesNotExist:
        if request.method == 'POST':
            form = AddFile(request.POST, request.FILES, initial={
                'user': _user,
                'work': _work
            })
            if form.is_valid():
                form.save()
                messages.success(request, f'Ответ к работе успешно выложен')
                return HttpResponseRedirect(reverse('works', kwargs={'id': id}))
        else:
            form = AddFile(initial={
                'user': _user,
                'work': _work
            })
        context = {
            'user': _user,
            'group': _group,
            'work': _work,
            'form': form,
        }
    return render(request, 'works/add_file.html', context=context)
