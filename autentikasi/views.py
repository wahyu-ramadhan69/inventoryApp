from inven.models import pegawai
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import login as auth_login
from .models import *
from .forms import *
from django.http import JsonResponse
import json
from django.contrib import messages


def index(request):
    context = {
        'page_title': 'LOGIN',
    }
    if request.method == "GET":
        if request.user.is_authenticated:
            if request.user.is_superuser == 1:
                return redirect('dashboard_admin')
            elif request.user.is_staff == 0:
                return redirect('dashboard_op')
        else:
            return render(request, 'auth/login.html', context)

    elif request.method == "POST":

        user = None
        username_login = request.POST['username']
        password_login = request.POST['password']

        user = authenticate(request, username=username_login,
                            password=password_login)

        if user is not None:
            auth_login(request, user)
            login(request, user)
            if user.is_superuser == 1:
                return redirect('dashboard_admin')
            elif user.is_staff == 0:
                return redirect('dashboard_op')
        else:
            messages.error(request, 'username atau password salah')
            return redirect('login')

    return render(request, 'auth/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('/')


def json(request):
    data = list(pegawai.objects.values())
    return JsonResponse(data, safe=False)


def lupa_pass(request):
    return render(request, 'auth/lupa_pass.html')


def eror(request):
    return render(request, 'eror.html')
