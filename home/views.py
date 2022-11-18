from django.shortcuts import render
from django.template import loader
from features.models import Members
from .forms import UserLogin,UserReg
from django.contrib import auth
from django.contrib.auth import authenticate,login
from django.shortcuts import render,redirect
from django.http import HttpResponse
# Create your views here.
def home(request):
    return render(request,'features/home.html')

def logout(request):
    auth.logout(request)
    return redirect("http://127.0.0.1:8500/")


def log(request):
    template = loader.get_template('features/login.html')
    if request.method=='POST':
        form=UserLogin(request.POST)
        if form.is_valid():

            data=form.cleaned_data
            username=data['username']
            password=data['password']
            user=authenticate(username=username,password=password)

            if user is not None:

                if user.is_active:
                    login(request,user)
                    return redirect('home/',request)

            return HttpResponse('<h1>Invalid Credentials</h1>')
        return HttpResponse('<h1>invalid Data</h1>')
    else:
        return HttpResponse(template.render({}, request))

def Reg(request):
    template = loader.get_template('features/Register.html')
    if request.method=='POST':
        form=UserReg(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            data=form.cleaned_data
            usr=data['username']
            pas=data['password']
            eml=data['email']
            nmb=data['number']
            a=Members()
            a.username=usr
            a.password=pas
            a.email=eml
            a.number=nmb
            a.save()
            user.set_password(pas)

            user.save()
            user=authenticate(username=usr,password=pas)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return render(request,'features/home.html')

            return HttpResponse('<h1>VALID</h1>')
        return HttpResponse(template.render({'form':form},request))
    else:
        return HttpResponse(template.render({},request))
