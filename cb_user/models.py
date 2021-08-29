from django.db import models

# Create your models here.
class UserInfo(models.Model):
    uname = models.CharField(max_length=20)
    upwd = models.CharField(max_length=40) # 存储加密后的长度为40
    uemail = models.CharField(max_length=30)
    # 收货人地址
    uaddr = models.CharField(max_length=20,default='')
    # 收货人详细地址
    uaddress = models.CharField(max_length=100,default='')
    # 邮编
    uyoubian = models.CharField(max_length=6,default='')
    uphone = models.CharField(max_length=11,default='')
    # 收货人
    ushou = models.CharField(max_length=20)