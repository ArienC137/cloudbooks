from django.db import models

# Create your models here.
class StarInfo(models.Model):
    user = models.ForeignKey('cb_user.UserInfo',on_delete=models.CASCADE)
    goods = models.ForeignKey('cb_goods.GoodsInfo',on_delete=models.CASCADE)
    # 收藏日期
    sdate = models.DateTimeField(auto_now_add=True)
