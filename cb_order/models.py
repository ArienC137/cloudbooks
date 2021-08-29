from django.db import models

# Create your models here.
# 订单主表
class OrderInfo(models.Model):
    # 订单编号
    oid = models.CharField(max_length=20,primary_key=True)
    # 下单用户
    user = models.ForeignKey('cb_user.UserInfo',on_delete=models.CASCADE)
    # 下单日期
    odate = models.DateTimeField(auto_now=True)
    # 收货地址：如果更改，就和编辑地址栏存的地址不一样了，所以需要存
    oaddress = models.CharField(max_length=150)
    # 是否支付
    oIsPay = models.BooleanField(default=False)
    # 总金额：因为使用频率高，所以存下来减轻做聚合运算的压力
    ototal = models.DecimalField(max_digits=6,decimal_places=2)

# 订单详表
class OrderDetailInfo(models.Model):
    # 和订单主表关联
    order = models.ForeignKey(OrderInfo,on_delete=models.CASCADE)
    # 购买的商品
    goods = models.ForeignKey('cb_goods.GoodsInfo',on_delete=models.CASCADE)
    # 购买商品的价格（单价）
    price = models.DecimalField(max_digits=5,decimal_places=2)
    # 购买的数量
    count = models.IntegerField()

# 支付方式：单独建一个提供的支付方式的类：然后和订单主表关联