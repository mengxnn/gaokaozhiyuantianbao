# your_app/urls.py
from django.urls import path
from . import views

app_name = 'loginRegister'  # 添加应用命名空间

urlpatterns = [
    path('map/', views.map, name='map'),
    path('bypart/', views.bypart, name='bypart'),
    path('api/scores/', views.get_scores, name='get_scores'),
]