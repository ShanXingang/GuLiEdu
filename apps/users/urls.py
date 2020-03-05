"""GuLiEdu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from .views import *

urlpatterns = [
     # 注册
     re_path(r'^user_register/$', user_register, name='user_register'),
     # 登陆
     re_path(r'^user_login/$', user_login, name='user_login'),
     # 注销
     re_path(r'user_logout/$',user_logout, name='user_logout'),
     # 激活邮箱验证码
     re_path(r'user_active/(\w+)/$', user_activate, name='user_activate'),
     # 忘记密码
     re_path(r'user_forget/$', user_forget, name='user_forget'),
     # 激活邮箱验证码
     re_path(r'user_reset/(\w+)/$', user_reset, name='user_reset'),

]
