from django.http import HttpResponse
from django.shortcuts import render
from loginRegister.models import RegisterUser
from django.shortcuts import redirect

# Create your views here.

def index(request):
    login_msg="恭喜！登录成功"
    return render(request,'index.html',{'login_msg':login_msg})

def register(request):
    if request.method=="POST":
        userName = request.POST.get("userName")
        userEmail=request.POST.get('userEmail')
        userPassword=request.POST.get('userPassword')
        userRePassword=request.POST.get('userRePassword')

        # 检查字段是否为空
        if not userName:
            error_msg = "用户名不能为空"
            return render(request, 'register.html', {'error_msg': error_msg})
        if not userEmail:
            error_msg = "邮箱不能为空"
            return render(request, 'register.html', {'error_msg': error_msg})
        if not userPassword:
            error_msg = "密码不能为空"
            return render(request, 'register.html', {'error_msg': error_msg})

        try:
            # 检查邮箱是否已存在
            Email = RegisterUser.objects.get(email=userEmail)
            error_msg = "邮箱已被注册"
            return render(request, 'register.html', {'error_msg': error_msg})
        except RegisterUser.DoesNotExist:
            # 如果邮箱不存在，继续检查用户名
            try:
                name = RegisterUser.objects.get(username=userName)
                error_msg = "用户名已存在"
                return render(request, 'register.html', {'error_msg': error_msg})
            except RegisterUser.DoesNotExist:
                # 两者都不存在，允许注册
                if userPassword != userRePassword:
                    error_msg = "两次密码不一致"
                    return render(request, 'register.html', {'error_msg': error_msg})
                else:
                    register = RegisterUser(email=userEmail, password=userPassword, username=userName)
                    register.save()
                    return redirect('/login/')
    else:
        return render(request,'register.html')

def login(request):
    if request.method=="POST":
        userName=request.POST.get("userName")
        # userEmail=request.POST.get('userName')
        userPassword=request.POST.get('userPassword')
        try:  #检查数据库中是否存在该用户
            # Email=RegisterUser.objects.get(email=userEmail)
            user=RegisterUser.objects.get(username=userName)  #使用用户名和密码验证登录
            if userPassword==user.password:  #密码正确，登录成功
                return redirect('/index/')
            else:
                error_msg="密码错误"
                return render(request,'login.html',{'error_msg':error_msg})
        except RegisterUser.DoesNotExist:  #数据库中不存在该用户
            error_msg="用户名不存在"
            return render(request,'login.html',{'error_msg':error_msg})
    else:
        return render(request, 'login.html')


