from django.urls import path
from . import views

urlpatterns = [
    path('', views.input_info, name='input_info'),  # 用于处理用户输入信息的页面
    path('recommendations/', views.recommendations, name='recommend_universities'),  # 用于推荐高校的页面

]
