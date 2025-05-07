# your_app/urls.py
from django.urls import path
from . import views

app_name = 'loginRegister'  # 添加应用命名空间

urlpatterns = [
    path('map/', views.map, name='map'),
    path('bypart/', views.bypart, name='bypart'),
    path('api/scores/', views.get_scores, name='get_scores'),
    path('login/', views.login),
    path('logout/', views.logout, name='logout'),
    path('index/', views.index),
    path('register/', views.register),
    path('profile/', views.profile, name='profile'),
    path('search_universities/', views.search_universities, name='search_universities'),
]