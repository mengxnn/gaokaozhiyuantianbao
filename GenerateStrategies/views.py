# -*- coding: utf-8 -*-
import numpy as np
from django.shortcuts import render
import pymysql
import pandas as pd
from django.http import JsonResponse
from django.shortcuts import render, redirect
from loginRegister.models import RegisterUser


# 数据库连接信息
DB_SCORE = {
    'host': 'localhost',  # 数据库地址（本地/远程）
    'user': 'root',  # 数据库用户名
    'password': '123456',  # 数据库密码
    'database': 'score',  # 数据库名
    'charset': 'utf8mb4',  # 设定编码，防止中文乱码
}

# 注意要修改湖北省表的信息
DB_YFYDB = {
    'host': 'localhost',  # 数据库地址（本地/远程）
    'user': 'root',  # 数据库用户名
    'password': '123456',  # 数据库密码
    'database': 'yfydb',  # 数据库名
    'charset': 'utf8mb4',  # 设定编码，防止中文乱码
}

valid_provinces = ['湖南', '湖北', '江苏']  # 所有支持的省份

def get_rank(request):
    if request.method == 'POST':
        province = request.POST.get('province')
        score = int(request.POST.get('score'))
        subject1 = request.POST.get('subject1')  # 获取物理/历史
        year = 2024

        if province not in valid_provinces:
            return JsonResponse({'error': '暂不支持该省份查询'}, status=400)

        connection = pymysql.connect(**DB_YFYDB)
        try:
            with connection.cursor() as cursor:
                # 查询大于等于该分数的最小累计排名
                query = f"""
                SELECT tot_num 
                FROM `{province}{subject1}类一分一段表`
                WHERE province = %s 
                    AND year = %s 
                    AND subject1 = %s
                    AND score <= %s
                ORDER BY score DESC 
                LIMIT 1
                """
                cursor.execute(query, (province, year, f"{subject1}类", score))
                result = cursor.fetchone()
                return JsonResponse({'rank': result[0] if result else None})

        except Exception as e:
            print(f"数据库查询异常：{str(e)}")
            return JsonResponse({'error': '服务器内部错误'}, status=500)
        finally:
            if connection:
                connection.close()

def input_info(request):
    if not request.session.get('is_authenticated'):
        return redirect('/login')
    user_id = request.session.get('user_id')
    user_data = {}
    try:
        user = RegisterUser.objects.get(id=user_id)
        user_data = {
            'province': user.province if hasattr(user, 'province') else '',
            'subject1': user.subject1 or '',
            'subject2': user.subject2 or '',
            'subject3': user.subject3 or '',
            'score': user.score if user.score else ''
        }
    except RegisterUser.DoesNotExist:
        request.session.flush()
        return redirect('/login')

    if request.method == 'POST':
        # 获取用户的输入数据
        user_score = int(request.POST.get('score'))  # 确保用户分数是整数
        user_rank = int(request.POST.get('rank'))
        user_province = request.POST.get('province')
        user_subjects = [request.POST.get('subject1'), request.POST.get('subject2'), request.POST.get('subject3')]
        filter_double_first = request.POST.get('double_first_class') == '1'  #是否只去双一流

        # 验证省份有效性
        if user_province not in valid_provinces:
            print("省份无效，触发错误提示")  # 检查控制台输出
            return render(request, 'input_info.html', {'error': '暂不支持该省份查询', 'user_data': user_data})

        table_name = f"`{user_province}招生情况`"

        # 连接数据库
        connection = pymysql.connect(**DB_SCORE)

        try:
            with connection.cursor() as cursor:
                # SQL 查询：获取专业分数线数据
                query = f"""
                    SELECT t1.school_name, major, t1.province,
                    ROUND(AVG(min_score),2) AS avg_score,
                    ROUND(AVG(lowest_rank),2) AS avg_rank,
                    sub_req, is985, is211, isdoubleFC
                    FROM {table_name} AS t1 JOIN `所有院校信息` AS t2
                    ON t1.school_name = t2.school_name
                    GROUP BY school_name, major, province, sub_req, is985, is211, isdoubleFC
                    ORDER BY avg_score DESC;
                """
                cursor.execute(query)
                data = cursor.fetchall()
        except pymysql.err.ProgrammingError as e:
            print(f"数据库查询异常：{str(e)}")
            return render(request, 'input_info.html', {'error': '该省份数据暂不可用', 'user_data': user_data})

        # 关闭数据库连接
        cursor.close()
        connection.close()

        # 转换为 Pandas DataFrame
        df = pd.DataFrame(data, columns=['school_name', 'major', 'province', 'avg_score',
                                         'avg_rank', 'sub_req', 'is985', 'is211', 'isdoubleFC'])

        # 添加分数和排名差距
        df['score_diff'] = (df['avg_score'] - user_score).round(2)
        df['rank_diff'] = (df['avg_rank'] - user_rank).round(2)

        # 定义分类边界
        chong_range = (user_score + 1, user_score + 15)
        wen_range = (user_score - 14, user_score)
        bao_range = (user_score - 30, user_score - 15)

        # 筛选满足分数要求的高校（保留原有分数范围）
        recommended_schools = df[
            (df['avg_score'] >= bao_range[0]) &
            (df['avg_score'] <= chong_range[1])
            ]

        # 新增分类逻辑
        recommended_schools['category'] = pd.cut(
            recommended_schools['avg_score'],
            bins=[-np.inf, bao_range[1], wen_range[1], chong_range[1], np.inf],
            labels=['可保底', '较稳妥', '可冲击', '超出范围']
        )

        # 过滤掉超出范围的记录
        recommended_schools = (
            recommended_schools[
            recommended_schools['category'] != '超出范围'
            ]
        )

        # 双一流筛选条件
        if filter_double_first:
            recommended_schools = recommended_schools[
                recommended_schools['isdoubleFC'] == '是'
            ]

        # 筛选符合选科要求的专业
        def filter_by_subject(row, selected_subjects):
            sub_req = row['sub_req']
            # 提取首选科目（如 "首选物理"）
            if "首选" in sub_req:
                first_subject = sub_req.split("，")[0].replace("首选", "").strip()  #按“，”分开；将“首选”替换成空串
                if first_subject not in selected_subjects:
                    return False  # 如果用户的选科不包含此首选科目，则不推荐

            # 提取再选科目要求
            if "再选" in sub_req:
                allowed_subjects = sub_req.split("，")[1].replace("再选", "").strip()
                if allowed_subjects != "不限":
                    allowed_subjects = allowed_subjects.split("/")  # 可能是 "化学/生物(2选1)"
                    if not any(sub in selected_subjects for sub in allowed_subjects):
                        return False  # 如果用户选科不匹配再选要求，则不推荐

            return True

        # 应用选科筛选
        recommended_schools = recommended_schools[recommended_schools.apply(
            lambda row: filter_by_subject(row, user_subjects), axis=1
        )]

        # 按学校进行分组，确保每个学校显示多个专业
        # 按分类和分数排序
        recommended_schools = recommended_schools.sort_values(
            by=['category', 'avg_score'],
            ascending=[True, False]
        )

        # 分组处理
        grouped_schools = {}
        for category in ['可冲击', '较稳妥', '可保底']:
            category_data = []
            # 按学校分组
            for school_name, school_df in recommended_schools[recommended_schools['category'] == category].groupby(
                    'school_name'):
                school_info = {
                    'name': school_name,
                    'majors': school_df.to_dict(orient='records')  # 包含所有专业信息
                }
                category_data.append(school_info)
            grouped_schools[category] = category_data  # 结构：{'冲': [学校1, 学校2...], ...}

        return render(request, 'recommendations.html', {
            'grouped_schools': grouped_schools,
            'user_score': user_score,
            'score_ranges': {
                '可冲击': chong_range,
                '较稳妥': wen_range,
                '可保底': bao_range
            },
            'categories': ['可冲击', '较稳妥', '可保底'],  # 新增分类列表
            'user': user,
        })

    return render(request, 'input_info.html', {'user_data': user_data,'user': user})

def recommendations(request):
    if not request.session.get('is_authenticated'):
        return redirect('/login')
    user_id = request.session.get('user_id')
    try:
        user = RegisterUser.objects.get(id=user_id)
    except RegisterUser.DoesNotExist:
        request.session.flush()
        return redirect('/login')
    return render(request, 'recommendations.html', {'user': user})