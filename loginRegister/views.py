from django.shortcuts import render
from loginRegister.models import RegisterUser
from django.shortcuts import redirect

# Create your views here.

def index(request):
    login_msg="恭喜！登录成功"
    return render(request,'index.html',{'login_msg':login_msg})

def register(request):
    if request.method=="POST":
        userEmail=request.POST.get('userEmail')
        userPassword=request.POST.get('userPassword')
        userRePassword=request.POST.get('userRePassword')
        try:  #数据库中已存在该用户
            user=RegisterUser.objects.get(reg_mail=userEmail)
            if user:
                msg="用户名已存在"
                return render(request,'register.html',{'msg':msg})
        except:  #数据库中不存在该用户，允许注册
            if userPassword!=userRePassword:  #检查密码和确认密码是否一致
                error_msg="密码不一致"
                return render(request,'register.html',{'error_msg':error_msg})
            else:
                register=RegisterUser(reg_mail=userEmail)
                register.reg_mail=userEmail
                register.reg_pwd=userPassword
                register.save()
                return redirect('/login/')
    else:
        return render(request,'register.html')

def login(request):
    if request.method=="GET":
        return render(request,'login.html')
    if request.method=="POST":
        userEmail=request.POST.get('username')
        userPassword=request.POST.get('userpassword')
        try:  #检查数据库中是否存在该用户
            user=RegisterUser.objects.get(reg_mail=userEmail)
            if userPassword==user.reg_pwd:  #密码正确，登录成功
                return redirect('/index/')
            else:
                error_msg="密码错误"
                return render(request,'login.html',{'error_msg':error_msg})
        except:  #数据库中不存在该用户
            error_msg="用户名不存在"
            return render(request,'login.html',{'error_msg':error_msg})