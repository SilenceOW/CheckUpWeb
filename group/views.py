from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from main.models import Group, Profile
from django.shortcuts import redirect
from operator import attrgetter
from .forms import AddUserForm, AddGroupForm
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib import messages

# Create your views here.


@login_required(login_url='/login')
def groups(request):
    _user = request.user
    _groups = _user.profile.groups.all()
    if _user.profile.groups.count() == 0:
        if request.method == 'POST':
            form = AddGroupForm(request.POST)
            if form.is_valid():
                _title = form.cleaned_data['title']
                _group = Group.objects.create(title=_title, creator=_user)
                messages.success(request, f'Группа "{_title}" была создана')
                return redirect('/groups')
        else:
            form = AddGroupForm()
        return render(request, 'group/no_groups.html', context={"form": form})

    if request.method == 'POST':
        form = AddGroupForm(request.POST)
        if form.is_valid():
            _title = form.cleaned_data['title']
            _group = Group.objects.create(title=_title, creator=_user)
            messages.success(request, f'Группа "{_title}" была создана')
            return redirect('/groups')
    form = AddGroupForm()
    return render(request, 'group/groups.html', context={"groups": _groups, "user": _user, "form": form})


# main.models.Profile.DoesNotExist


@login_required(login_url='/login')
def group(request, id):
    _user = request.user
    user_group = get_object_or_404(_user.profile.groups, id=id)
    group_users = user_group.profile_set.all().exclude(id=user_group.creator.id)
    sorted_group_users = sorted(group_users, key=attrgetter('user.last_name'))
    form = AddUserForm(request.POST or None)
    context = {
        "group": user_group,
        "users": sorted_group_users,
        "user": _user,
        "form": form
    }
    if form.is_valid():
        print('form is valid')
        username = form.cleaned_data['username']
        user_profile = get_object_or_404(User.objects, username=username).profile
        user_group.profile_set.add(user_profile)
        messages.success(request, f'{username} был добавлен в группу')
        return HttpResponseRedirect(reverse('group', kwargs={'id': id}))

    return render(request, 'group/group.html', context=context)


@login_required(login_url='/login')
def leave_group(request, pk):
    _user = request.user
    _group = get_object_or_404(_user.profile.groups, id=pk)
    _user.profile.groups.remove(_group)
    messages.success(request, f'Вы покинули группу "{_group}"')
    return redirect('/groups')


@login_required(login_url='/login')
def kick_user(request, id, pk):
    _user = User.objects.get(id=pk)
    user_group = get_object_or_404(_user.profile.groups, id=id)
    creator_id = user_group.creator.id
    user_id = request.user.id
    _user.profile.groups.remove(user_group)
    messages.success(request, f'{_user} больше не в "{user_group}"')
    return redirect(reverse('group', kwargs={'id': id}))
