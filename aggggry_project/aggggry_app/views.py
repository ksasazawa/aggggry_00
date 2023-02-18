from django.shortcuts import render, redirect
import os
import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Jobs

# Create your views here.

def home(request):
    jobs = Jobs.objects.all()
    return render(request, 'aggggry_app/home.html', context = {
        "jobs": jobs
        })
