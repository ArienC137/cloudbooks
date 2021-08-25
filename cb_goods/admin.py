from django.contrib import admin
from .models import *

# Register your models here.
# 定义一个继承admin.ModelAdmin类的子类TypeInfoAdmin
class TypeInfoAdmin(admin.ModelAdmin):
    # 显示字段：显示后可以点击列头进行排序
    list_display = ['id','ttitle'] # 要填写模型类中有的字段：一定有id（迁移文件中自带），填写的字段的顺序就是显示顺序。

class GoodsInfoAdmin(admin.ModelAdmin):
    # 分页：一页显示多少条数据，分页框会出现在下侧
    list_per_page = 15
    list_display = ['id','gtitle','gprice','gsellprice','gauthor','gpublish','gpubtime','gclick','gstock','gtype']

# 向里面注册模型类：admin.site.register(模型类,admin类)
admin.site.register(TypeInfo,TypeInfoAdmin) # 要把Admin类注册进去才能显示
admin.site.register(GoodsInfo,GoodsInfoAdmin)