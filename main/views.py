from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from django.template import RequestContext


@login_required(login_url='/login')
def home(request):
    _user = request.user

    context = {
        'user': _user
    }
    return render(request, 'main/home.html', context=context)


def custom_page_not_found_view(request, exception):
    return render(request, "errors/404.html", {})


def custom_error_view(request, exception=None):
    return render(request, "errors/500.html", {})


def custom_permission_denied_view(request, exception=None):
    return render(request, "errors/403.html", {})


def custom_bad_request_view(request, exception=None):
    return render(request, "errors/400.html", {})