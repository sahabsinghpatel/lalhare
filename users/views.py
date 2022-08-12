import imp
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Profile, Temp_User
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import random
from hashlib import sha256
from django.contrib import messages

def index(request):
    un=request.user
    user=User.objects.get(username=un)
    profile=Profile.objects.get(user=user)
    return render(request, "index.html", context={'profile':profile})

def register(request):
    if request.user.is_authenticated:
        return redirect('/users/')
    else:
        if request.method=='POST':
            un=request.POST.get('un')
            em=request.POST.get('em')
            pswd=request.POST.get('pass')
            user=User.objects.create(username=un, email=em)
            user.set_password(pswd)
            user.save()
            login(request, user)
            #profile
            phone=request.POST.get('phone')
            dob=request.POST.get('dob')
            profile=Profile.objects.create(user=user, phone=phone, birth_date=dob)
            profile.save()
            return redirect('/')
        else:
            return render(request, 'users/register.html')

def login_user(request):
    if request.user.is_authenticated:
        return redirect('/users/')
    else:
        if request.method=='POST':
            em=request.POST.get('em')
            pswd=request.POST.get('pswd')
            user=authenticate(username=em, password=pswd)
            print(user, em, pswd)
            if user is not None:
                login(request, user)
                return redirect('/')
            return redirect('/users/register/')
        return render(request, 'users/login.html')

@login_required(login_url="users/login/")
def logout_user(request):
    logout(request)
    return redirect('/users/login/')

def loginWithOTP(request):
    if request.method=="POST":
        token=request.POST.get("token")
        otp=int(request.POST.get('otp'))
        try:
            temp_user=Temp_User.objects.get(token=token)
            if otp==temp_user.otp:
                user=User.objects.get(email=temp_user.email)
                login(request, user)
                temp_user.delete()
                return redirect('/')
            return render(request, 'logins/login-with-otp.html', {'token':token})
        except Exception as E:
            return redirect('/login')

@login_required(login_url='/login')
def chpass(request):
    if request.method=="POST":
        old_pass=request.POST.get("pass_now")
        new_pass=request.POST.get("new_pass")
        email=request.user.email
        user=authenticate(email=email, password=old_pass)
        if user is not None:
            user=User.objects.get(email=email)
            user.set_password(new_pass)
            user.save()
            login(request, user)
            messages.success(request, 'Password changed successfully')
            return redirect('/')
        messages.success(request, 'Invalid Password')
        return redirect('/')
    return redirect('/')



def otpGen():
    return random.randint(100000, 999999)

def tokenGen():
    token=str(random.random())
    return sha256(token.encode('utf-8')).hexdigest()
