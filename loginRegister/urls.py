# your_app/urls.py
from django.urls import path
from . import views

app_name = 'loginRegister'  # ���Ӧ�������ռ�

urlpatterns = [
    path('map/', views.map, name='map'),
    path('bypart/', views.bypart, name='bypart'),
    path('api/scores/', views.get_scores, name='get_scores'),
]