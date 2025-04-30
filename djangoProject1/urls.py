"""
URL configuration for djangoProject1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from django.urls import path, include
from loginRegister import views

#添加网页时要在这里添加对应的path
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('loginRegister.urls')),  # 包括 loginRegister 应用的 URL 路由
    path('GenerateStrategies/', include('GenerateStrategies.urls')),  # 包括 GenerateStrategies 应用的 URL 路由
]
