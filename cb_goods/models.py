from django.db import models
from tinymce.models import HTMLField

# Create your models here.
# 商品分类
class TypeInfo(models.Model):
    ttitle = models.CharField(max_length=20)
    # 逻辑删除：默认不删
    isDelete = models.BooleanField(default=False)
    # 输入中文时出现错误，所以需要编码。Django定义模型类转换成字符串的方式：python2使用self.ttitle.encode('utf-8')，python3使用self.ttitle。
    def __str__(self):
        return self.ttitle

# 商品信息
class GoodsInfo(models.Model):
    # 商品名称
    gtitle = models.CharField(max_length=100)
    # 商品图片
    gpic = models.ImageField(upload_to='cb_goods')
    # 商品定价：使用decimal类型存储
    gprice = models.DecimalField(max_digits=5,decimal_places=2)
    # 商品售价：使用decimal类型存储
    gsellprice = models.DecimalField(max_digits=5,decimal_places=2)
    # 商品折扣：使用decimal类型存储
    gdiscount = models.DecimalField(max_digits=2,decimal_places=1,default=1)
    isDelete = models.BooleanField(default=False)
    # 作者：字符串类型
    gauthor = models.CharField(max_length=80)
    # 出版社：字符串类型
    gpublish = models.CharField(max_length=20)
    # 出版时间：字符串类型
    gpubtime = models.CharField(max_length=20)
    # 人气：按点击量（如果要按销量，需要每次从订单中使用聚合函数，为了减少服务器的压力，单独设计一个销量的字段）
    gclick = models.IntegerField()
    # 商品简介
    gbrief = models.CharField(max_length=200)
    # 库存（如果需要则设计）
    gstock = models.IntegerField()
    # 商品详情：使用富文本编辑器，方便编辑人员维护信息
    gdetail = HTMLField()
    # 内容简介
    gcontent = HTMLField()
    # 作者简介
    gauthorIntroduct = HTMLField()
    # 目录
    gcatalogue = HTMLField()
    # 商品分类
    gtype = models.ForeignKey(TypeInfo,on_delete=models.CASCADE)
    # 推荐商品：使用布尔类型而不使用整型（使用整型需要该商品的源代码的数值），默认不推荐
    # gadv = models.BooleanField(default=False)
    def __str__(self):
        return self.gtitle