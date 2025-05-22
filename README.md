### 开发环境：
    pycharm版本：2023.3.7
    bootstrap版本：3.3.7（bootstrap3需要依赖jquery）
    数据库相关：mysql 8.0，navicat 16
    Django版本：5.1.6，更新版本应该不影响使用

### 本地mysql配置：
    用户名：root
    端口号：3306
    IP：localhost
    密码：123456

### 数据库配置
    需要将excel文件导入数据库中。
    数据库名：score，表名：湖南/湖北/江苏招生情况
    数据库名：yfydb，表名：{province}{subject}类一分一段表

    新建查询，使用命令：
    UPDATE `（湖北）一分一段表` SET subject1='历史类' WHERE subject1='历史';
    将“历史”改成“历史类”，否则不能查询湖北省历史类的分数线

    先新建register_info数据库，再使用命令：
    python manage.py makemigrations
    python manage.py migrate

    register_info中的表loginregister_yfydtable需要导入一分一段总表，即各省份一起导入

### 其他注意事项
    若一分一段表显示中文乱码，需要将bypart.js保存为utf-8格式
    bypart是一分一段表页面