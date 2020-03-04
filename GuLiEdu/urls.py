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
import xadmin

# 使用include的目的是为了使代码整洁，当有users开头的请求来访问，我们把它转到users模块中去分发，在users模块里面也有一个urlpatterns对请求进行处理
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('xadmin/',xadmin.site.urls),
    re_path(r'^users/', include(('users.urls', 'users'), namespace='users')),
    re_path(r'^courses/', include(('courses.urls', 'courses'), namespace='courses')),
    re_path(r'^orgs/', include(('orgs.urls', 'orgs'), namespace='orgs')),
    re_path(r'^operations/', include(('operations.urls', 'operations'), namespace='operations'))
]
