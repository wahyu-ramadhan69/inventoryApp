from django.shortcuts import render, redirect, HttpResponse, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from .models import *
from django.http import JsonResponse
import json


def json(request):
    data = list(pegawai.objects.values())
    return JsonResponse(data, safe=False)
