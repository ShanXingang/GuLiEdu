from django.shortcuts import render, redirect, reverse
from .forms import UserRegisterForm, UserLoginForm
from .models import UserProfile
from django.db.models import Q
from django.contrib.auth import authenticate, logout, login

# Create your views here.
def index(request):
    return render(request, 'index.html')

def user_register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else :
        user_register_form = UserRegisterForm(request.POST)
        if user_register_form.is_valid():
            email = user_register_form.cleaned_data['email']
            password = user_register_form.cleaned_data['password']
            # 先查找用户表中是否有这个用户
            user_list = UserProfile.objects.filter(Q(username=email) | Q(email=email))
            if user_list:
                return render(request, 'register.html', {
                    'msg': '用户已经存在'
                })
            else:
                a = UserProfile()
                a.username = email
                a.set_password(password)
                a.email = email
                a.save()
                return redirect(reverse('index'))
        else:
            return render(request, 'register.html', {
                'user_register_form': user_register_form
            })

def user_login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        print('000')
        user_login_form = UserLoginForm(request.POST)
        if user_login_form.is_valid():
            email = user_login_form.cleaned_data['email']
            password = user_login_form.cleaned_data['password']

            # authenticate验证的就是username的字段
            user = authenticate(username=email, password=password)
            if user:
                print('111')
                login(request, user)
                return redirect(reverse('index'))
            else:
                print('222')
                return render(request, 'login.html',{
                    'msg': '邮箱或者密码有误'
                })
        else:
            print('333')
            return render(request, 'login.html', {
                'user_login_form': user_login_form
            })