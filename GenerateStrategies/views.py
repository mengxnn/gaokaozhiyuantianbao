from django.shortcuts import render
import pymysql
import pandas as pd
from django.http import JsonResponse

# 数据库连接信息
DB_CONFIG = {
    'host': 'localhost',  # 数据库地址（本地/远程）
    'user': 'root',  # 数据库用户名
    'password': '123456',  # 数据库密码
    'database': 'score',  # 数据库名
    'charset': 'utf8mb4',  # 设定编码，防止中文乱码
}


def get_rank(request):
    if request.method == 'POST':
        province = request.POST.get('province')
        score = int(request.POST.get('score'))
        subject1 = request.POST.get('subject1')  # 获取物理/历史
        year = 2024  # 使用最新年份数据

        connection = pymysql.connect(**DB_CONFIG)
        try:
            with connection.cursor() as cursor:
                # 查询大于等于该分数的最小累计排名
                query = """
                SELECT tot_num 
                FROM `一分一段表`
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
    if request.method == 'POST':
        # 获取用户的输入数据
        user_score = int(request.POST.get('score'))  # 确保用户分数是整数
        user_rank = int(request.POST.get('rank'))
        user_province = request.POST.get('province')
        user_subjects = [request.POST.get('subject1'), request.POST.get('subject2'), request.POST.get('subject3')]

        # 连接数据库
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor()

        # SQL 查询：获取 2021-2023 年数据，并计算各专业的平均分
        query = """
            SELECT school_name, major, province, ROUND(AVG(min_score),2) AS avg_score, ROUND(AVG(lowest_rank),2) AS avg_rank, sub_req, is985, is211, isdoubleFC
            FROM `2021-2023湖南省招生情况` NATURAL JOIN `所有院校信息`
            WHERE year IN (2021, 2022, 2023)
            GROUP BY school_name, major, province, sub_req
            ORDER BY avg_score DESC;
        """
        cursor.execute(query)
        data = cursor.fetchall()

        # 转换为 Pandas DataFrame
        df = pd.DataFrame(data, columns=['school_name', 'major', 'province', 'avg_score', 'avg_rank', 'sub_req', 'is985', 'is211', 'isdoubleFC'])

        #添加分数和排名差距
        df['score_diff'] = df['avg_score'] - user_score
        df['rank_diff'] = df['avg_rank'] - user_rank

        # 筛选满足分数要求的高校
        recommended_schools = df[
            (df['avg_score'] >= (user_score - 60)) & (df['avg_score'] <= (user_score + 20))
        ]

        # 筛选符合选科要求的专业
        def filter_by_subject(row, selected_subjects):
            sub_req = row['sub_req']
            #print(sub_req)
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

        # 关闭数据库连接
        cursor.close()
        connection.close()

        # 按学校进行分组，确保每个学校显示多个专业
        grouped_schools = recommended_schools.groupby('school_name').apply(
            lambda x: x.to_dict(orient='records')).reset_index()
        #print(grouped_schools)
        # 转换为列表形式，方便模板使用
        grouped_schools = grouped_schools[['school_name', 0]].to_dict(orient='records')
        #print(grouped_schools)
        # 返回推荐的高校
        return render(request, 'recommendations.html', {
            'grouped_schools': grouped_schools
        })

    return render(request, 'input_info.html')


def recommendations(request):
    recommend_msg = "推荐信息"
    return render(request, 'recommendations.html', {'login_msg': recommend_msg})