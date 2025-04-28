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
    否则不能查询湖北省历史类的分数线

    先新建register_info数据库，再使用命令：
    python manage.py makemigrations
    python manage.py migrate

    若之前已进行迁移，需要手动修改表的格式：
    ALTER TABLE loginRegister_registeruser
    ADD isvip BOOLEAN DEFAULT FALSE,
    ADD phone VARCHAR(20),
    ADD score INTEGER DEFAULT 0,
    ADD subject1 VARCHAR(10),
    ADD subject2 VARCHAR(10),
    ADD subject3 VARCHAR(10);

    register_info中的表loginregister_yfydtable需要导入一分一段总表，即各省份一起导入

### 其他注意事项
    若一分一段表显示中文乱码，需要将bypart.js保存为utf-8格式