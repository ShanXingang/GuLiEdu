from django.shortcuts import render, redirect, reverse, HttpResponse
from .forms import *
from .models import UserProfile, EmailVerifyCode
from django.db.models import Q
from django.contrib.auth import authenticate, logout, login
from utils.send_mail_tool import send_email_code

# Create your views here.
def index(request):
    return render(request, 'index.html')

def user_register(request):
    if request.method == 'GET':
        user_register_form = UserRegisterForm() # 是为了使用验证码
        return render(request, 'register.html', {
            'user_register_form': user_register_form
        })
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
                send_email_code(email, 1)
                return HttpResponse('请尽快前往您的邮箱激活，否则无法登陆')
        else:
            return render(request, 'register.html', {
                'user_register_form': user_register_form
            })

def user_login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        user_login_form = UserLoginForm(request.POST)
        if user_login_form.is_valid():
            email = user_login_form.cleaned_data['email']
            password = user_login_form.cleaned_data['password']
            # authenticate验证的就是username的字段
            user = authenticate(username=email, password=password)
            if user:
                if user.is_start:
                    login(request, user)
                    return redirect(reverse('index'))
                else:
                    return HttpResponse('请去您的邮箱激活，否则无法登陆')
            else:
                return render(request, 'login.html',{
                    'msg': '邮箱或者密码有误'
                })
        else:
            return render(request, 'login.html', {
                'user_login_form': user_login_form
            })

def user_logout(request):
    logout(request)
    return redirect(reverse('index'))

def user_activate(request, code):
    if code:
        email_ver_list = EmailVerifyCode.objects.filter(code=code)
        if email_ver_list:
            email_ver = email_ver_list[0]
            email = email_ver.email
            user_list = UserProfile.objects.filter(email=email)
            if user_list:
                user = user_list[0]
                user.is_start = True
                user.save()
                return redirect(reverse('users:user_login'))
            else:
                pass
        else:
            pass
    else:
        pass

def user_forget(request):
    if request.method == 'GET':
        user_forget_form = UserForgetForm()
        return render(request, 'forgetpwd.html', {
            'user_forget_form': user_forget_form
        })
    else:
        user_forget_form = UserForgetForm(request.POST)
        if user_forget_form.is_valid():
            email = user_forget_form.cleaned_data['email']
            user_list = UserProfile.objects.filter(email=email)
            if user_list:
                send_email_code(email, 2)
                return HttpResponse('请尽快去您的邮箱重置密码')
            else:
                return render(request, 'forgetpwd.html',{
                    'msg': '用户不存在'
                })
        else:
            return render(request, 'forgetpwd.html', {
                'user_forget_form': user_forget_form
            })

def user_reset(request, code):
    print('AAA')
    if request.method == 'GET':
        return render(request, 'password_reset.html', {
            'code': code
        })
    else:
        print('000')
        print(code)
        user_reset_form = UserResetForm(request.POST)
        if user_reset_form.is_valid():
            print('111')
            password = user_reset_form.cleaned_data['password']
            password1 = user_reset_form.cleaned_data['password1']
            if password == password1:
                print('222')
                email_var_list = EmailVerifyCode.objects.filter(code=code)
                if email_var_list:
                    print('333')
                    email_var = email_var_list[0]
                    email = email_var.email
                    print(email)
                    user_list = UserProfile.objects.filter(email=email)
                    if user_list:
                        print('444')
                        user = user_list[0]
                        print(user.email)
                        user.set_password(password)
                        user.save()
                        return redirect(reverse('users:user_login'))
                    else:
                        print('555')
                        pass
                else:
                    print('666')
                    pass
            else:
                print('777')
                return render(request, 'password_reset.html', {
                    'msg': '两次密码不一致',
                    'code': code
                })
        else:
            print('888')
            return render(request, 'password_reset.html',{
                'user_reset_form': 'user_reset_form',
                'code': code
            })