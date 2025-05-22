from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from loginRegister.models import RegisterUser,YFYDTable
from django.shortcuts import redirect
from django.contrib import messages
import mysql.connector
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index(request):
    user = None
    if request.session.get('is_authenticated'):
        try:
            user_id = request.session.get('user_id')
            user = RegisterUser.objects.get(id=user_id)
        except RegisterUser.DoesNotExist:
            # 如果用户不存在，清除会话
            request.session.flush()
    return render(request, 'index.html', {'user': user})

def profile(request):
    if not request.session.get('is_authenticated'):
        return redirect('login')
    user_id = request.session.get('user_id')
    try:
        user = RegisterUser.objects.get(id=user_id)
    except RegisterUser.DoesNotExist:
        request.session.flush()
        return redirect('login')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        province=request.POST.get('province')
        subject1 = request.POST.get('subject1')
        subject2 = request.POST.get('subject2')
        subject3 = request.POST.get('subject3')
        score=request.POST.get('score')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        if not username or not email:
            return render(request, 'profile.html', {'user': user, 'error': '用户名和邮箱不能为空'})
        if RegisterUser.objects.filter(username=username).exclude(id=user.id).exists():
            return render(request, 'profile.html', {'user': user, 'error': '用户名已存在'})
        if RegisterUser.objects.filter(email=email).exclude(id=user.id).exists():
            return render(request, 'profile.html', {'user': user, 'error': '邮箱已存在'})
        if new_password and confirm_password:
            if new_password != confirm_password:
                return render(request, 'profile.html', {'user': user, 'error': '新密码不匹配'})
            else:
                user.password = new_password
        user.username = username
        user.email = email
        user.phone = phone
        user.province = province
        user.subject1 = subject1
        user.subject2 = subject2
        user.subject3 = subject3
        user.score = score
        user.save()
        request.session['username'] = username  # 更新会话中的用户名
        messages.success(request, '修改信息成功')
        return redirect('/profile')
    else:
        return render(request, 'profile.html', {'user': user})

def map(request):
    return render(request,'map.html')

def bypart(request):
    user = None
    if request.session.get('is_authenticated'):
        try:
            user_id = request.session.get('user_id')
            user = RegisterUser.objects.get(id=user_id)
        except RegisterUser.DoesNotExist:
            # 如果用户不存在，清除会话
            request.session.flush()
    return render(request, 'bypart.html', {'user': user})

def get_scores(request):
    data = list(YFYDTable.objects.all().values(
        'year', 'province', 'subject1', 'score', 'num', 'tot_num'
    ))
    return JsonResponse(data, safe=False)

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
        userPassword=request.POST.get('userPassword')
        try:  #检查数据库中是否存在该用户
            user=RegisterUser.objects.get(username=userName)  #使用用户名和密码验证登录
            if userPassword==user.password:  #密码正确，登录成功
                # 登录成功，保存用户信息到会话
                request.session['user_id'] = user.id
                request.session['username'] = user.username
                request.session['is_authenticated'] = True
                return redirect('/index/')
            else:
                error_msg="密码错误"
                return render(request,'login.html',{'error_msg':error_msg})
        except RegisterUser.DoesNotExist:  #数据库中不存在该用户
            error_msg="用户名不存在"
            return render(request,'login.html',{'error_msg':error_msg})
    else:
        return render(request, 'login.html')

def logout(request):
    # 清除会话
    request.session.flush()
    return redirect('/index/')


# 添加新的高校查询视图
def search_universities(request):
    user = None
    if request.session.get('is_authenticated'):
        try:
            user_id = request.session.get('user_id')
            user = RegisterUser.objects.get(id=user_id)
        except RegisterUser.DoesNotExist:
            # 如果用户不存在，清除会话
            request.session.flush()

    try:
        # 连接数据库
        db_conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='123456',
            database='score',
            charset='utf8mb4'
        )
        cursor = db_conn.cursor(dictionary=True)

        # 获取过滤参数
        search_query = request.GET.get('search', '')
        province = request.GET.get('province', '')
        school_type = request.GET.get('school_type', '')
        department = request.GET.get('department', '')
        characteristics = request.GET.getlist('characteristics')  # 获取多选的院校特色

        # 基础SQL查询
        sql = "SELECT * FROM 所有院校信息 WHERE 1=1"
        params = []

        # 添加过滤条件
        if search_query:
            sql += " AND school_name LIKE %s"
            params.append(f'%{search_query}%')

        if province:
            sql += " AND province = %s"
            params.append(province)

        if school_type:
            sql += " AND type = %s"
            params.append(school_type)

        if department:
            sql += " AND nature = %s"
            params.append(department)

        if characteristics:
            char_conditions = []
            for char in characteristics:
                if char == '985':
                    char_conditions.append("is985 = '是'")
                elif char == '211':
                    char_conditions.append("is211 = '是'")
                elif char == '双一流':
                    char_conditions.append("isdoubleFC = '是'")
            if char_conditions:
                sql += " AND (" + " AND ".join(char_conditions) + ")"

        # 排序
        sql += " ORDER BY school_name"

        # 执行查询
        cursor.execute(sql, params)
        universities = cursor.fetchall()

        # 获取下拉筛选器的唯一值
        cursor.execute("SELECT DISTINCT province FROM 所有院校信息 ORDER BY province")
        provinces = [row['province'] for row in cursor.fetchall()]

        cursor.execute("SELECT DISTINCT type FROM 所有院校信息 ORDER BY type")
        school_types = [row['type'] for row in cursor.fetchall()]

        cursor.execute("SELECT DISTINCT nature FROM 所有院校信息 ORDER BY nature")
        departments = [row['nature'] for row in cursor.fetchall()]

        # 分页处理
        page = request.GET.get('page', 1)
        paginator = Paginator(universities, 20)  # 每页显示20所高校

        try:
            universities_page = paginator.page(page)
        except PageNotAnInteger:
            universities_page = paginator.page(1)
        except EmptyPage:
            universities_page = paginator.page(paginator.num_pages)

        context = {
            'universities': universities_page,
            'provinces': provinces,
            'school_types': school_types,
            'departments': departments,
            'search_query': search_query,
            'selected_province': province,
            'selected_school_type': school_type,
            'selected_department': department,
            'selected_characteristics': characteristics,
            'user': user,
        }

    except mysql.connector.Error as err:
        context = {
            'error': f"数据库错误: {err}",
            'user': request.user,
        }
    finally:
        # 关闭数据库连接
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'db_conn' in locals() and db_conn:
            db_conn.close()



    return render(request, 'search_universities.html', context)
