### 本地mysql配置：
    用户名：root
    端口号：3306
    IP：localhost
    密码：123456

### 数据库配置
    需要将excel文件导入数据库中。
    数据库名：score
    表名：2022-2024湖南/湖北/江苏招生情况
    新建查询，使用命令：
    UPDATE `一分一段表` SET subject1='历史类' WHERE subject1='历史';
    否则不能查询湖北省历史类的分数线

    先新建register_info数据库，再使用命令：
    python manage.py makemigrations
    python manage.py migrate
