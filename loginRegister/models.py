from django.db import models

# Create your models here.

class RegisterUser(models.Model):
    email=models.EmailField(max_length=100,unique=True,default='default@example.com')
    # email = models.EmailField()
    password=models.CharField(max_length=32,default='123456')
    username=models.CharField(max_length=100,unique=True,default='default_username')

    def __str__(self):
        return self.username