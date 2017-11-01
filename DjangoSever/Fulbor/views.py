from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib import auth
from django.template.context import RequestContext
from django.contrib.auth.models import User

from .forms import LoginForm, SignupForm


def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render_to_response('login.html', RequestContext(request, {'form': form, }))
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                return render_to_response('index.html', RequestContext(request))
            else:
                return render_to_response('login.html',
                                          RequestContext(request, {'form': form, 'password_is_wrong': True}))
        else:
            return render_to_response('login.html', RequestContext(request, {'form': form, }))


def signup(request):
    if request.method == 'GET':
        form = SignupForm
        return render_to_response('signup.html', RequestContext(request, {'form': form}))
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            if User.objects.filter(username=username).exists():
                return render_to_response('signup.html',
                                          RequestContext(request, {'form': form, 'username_exist': True}))
            user = User.objects.create_user(username=username, password=password)
            user.save()
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return render_to_response('index.html', RequestContext(request))
        else:
            return render_to_response('signup.html', RequestContext(request, {'form': form}))


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")
