from django.db import models

# Create your models here.
class CartInfo(models.Model):
    user = models.ForeignKey('cb_user.UserInfo',on_delete=models.CASCADE) # 外键关联的模型类如果定义在同一个应用中，直接写模型类名，否则要写成应用名.模型类名
    goods = models.ForeignKey('cb_goods.GoodsInfo',on_delete=models.CASCADE)
    count = models.IntegerField()
