from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from t_dist.models import Students

# Create your views here.

def home(request):
    if request.user.is_authenticated:
        return render(request,'home.html', {'user': request.user.username})
    else:
        return redirect("login")


def user_login(request):
    if request.method=="GET":
        if request.user.is_authenticated:
            return redirect("home")
        else:
            return render(request, "login.html")
    elif request.method=="POST":
        username = request.POST["u_name"]
        password = request.POST["password"]
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect("home")
        else:
            return render( request,"login.html",{'status': 1})


def user_logout(request):
    logout(request)
    return redirect("home")

