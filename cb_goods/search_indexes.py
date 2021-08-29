from haystack import indexes
from .models import GoodsInfo

# 指定对某个类的某些数据建立索引
class GoodsInfoIndex(indexes.SearchIndex,indexes.Indexable):
    # 对某个类型的字段进行检索
    text = indexes.CharField(document=True,use_template=True)
    def get_model(self):
        # 获取某个类对象
        return GoodsInfo

    def index_queryset(self,using=None):
        # 对哪些数据进行检索
        return self.get_model().objects.all() # 对GoodsInfo.objects.all()进行检索
