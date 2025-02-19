from django.db import models

# Create your models here.

class RegisterUser(models.Model):
    reg_mail=models.CharField(max_length=100,blank=False)
    reg_pwd=models.CharField(max_length=100,blank=False)