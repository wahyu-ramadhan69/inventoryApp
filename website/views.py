from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from django.contrib import messages


def test(request):
    return render(request, 'test.html')

def landing(request):
    return render(request, 'landing.html')