from django.db import models

# Create your models here.

class RegisterUser(models.Model):
    email=models.EmailField(max_length=100,unique=True,blank=False)
    password=models.CharField(max_length=32,blank=False)
    username=models.CharField(max_length=50,unique=True,blank=False)
    isvip=models.BooleanField(default=False)
    phone=models.CharField(max_length=20, null=True, default='')
    score=models.IntegerField(default=0)
    subject1=models.CharField(max_length=10, null=True, default='')
    subject2 = models.CharField(max_length=10, null=True, default='')
    subject3 = models.CharField(max_length=10, null=True, default='')

    def __str__(self):
        return self.username

class YFYDTable(models.Model):
    year = models.IntegerField()
    province = models.CharField(max_length=20)
    subject1 = models.CharField(max_length=10)  # 文理科类型
    score = models.IntegerField()  # 分数
    num = models.IntegerField()  # 本段人数
    tot_num = models.IntegerField()  # 累计人数

