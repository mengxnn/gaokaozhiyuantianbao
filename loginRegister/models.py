from django.db import models

# Create your models here.

class RegisterUser(models.Model):
    email=models.EmailField(max_length=100,unique=True,blank=False)
    password=models.CharField(max_length=32,blank=False)
    username=models.CharField(max_length=100,unique=True,blank=False)

    def __str__(self):
        return self.username