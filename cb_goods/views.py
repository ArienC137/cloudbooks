from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from cb_goods.models import *
from cb_cart.models import *
from django.core.paginator import *
import time

# Create your views here.
# 购物车数量
def cart_count(request):
    if request.session.has_key('user_id'):
        # 查询当前登录用户的所有购物车信息
        return CartInfo.objects.filter(user_id=request.session['user_id'])
    else:
        return 0

def list(request,tid,pindex,sort): # tid是类型，pindex是当前页数，sort是排序依据
    # 根据分类的id查询类型信息
    typeinfo = TypeInfo.objects.get(pk=int(tid))
    # 新品推荐：按id名降序排序，取前2条数据
    news = typeinfo.goodsinfo_set.order_by('-id')[0:2]
    # 当前商品的分类对应的特价书榜：按折扣升序排序，取前10条数据
    disc = typeinfo.goodsinfo_set.order_by('gdiscount')[0:10]
    # 默认（最新）
    if sort == '1':
        goods_list = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-id')
        title = str(typeinfo.ttitle) + '默认'
    # 价格
    if sort == '2':
        goods_list = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-gsellprice')
        title = str(typeinfo.ttitle) + '价格'
    # 人气（点击量）
    if sort == '3':
        goods_list = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-gclick')
        title = str(typeinfo.ttitle) + '人气'
    # 分页：Paginator(列表,int)
    paginator = Paginator(goods_list,10) # 一页放10条数据
    # 显示当前页的数据
    page = paginator.page(int(pindex))
    carts = cart_count(request)
    context = {'title':title,
               'page':page,'paginator':paginator,
               'typeinfo':typeinfo,'sort':sort,
               'news':news,'disc':disc,'carts':carts
               }
    return render(request,'cb_goods/list.html',context) # 显示列表页

def detail(request,id):
    # 获取当前日期
    datetime = time.strftime("%m/%d")
    # 根据id查询商品
    goods = GoodsInfo.objects.get(pk=int(id))
    # 点击量+1
    goods.gclick = goods.gclick + 1
    # 当前商品的分类对应的特价书榜：按折扣升序排序，取前4条数据
    goods.gdiscount = goods.gsellprice*10//goods.gprice
    goods.save()
    disc = goods.gtype.goodsinfo_set.order_by('gdiscount')[0:4]
    carts = cart_count(request)
    context = {'title':goods.gtitle,'g':goods,'id':id,'disc':disc,'carts':carts}
    response = render(request,'cb_goods/detail.html',context) # 显示详情页
    # 记录浏览记录，在用户中心使用：使用datetime作为键记录日期，获取datetime键对应的值，第一次为空
    goods_ids = request.COOKIES.get('goods_ids','')
    # 取goods.id的字符串形式
    goods_id = '%d'%goods.id
    # 判断是否有浏览记录
    if goods_ids != '':
        # 用“,”分隔为列表（拼接的时候就是用“,”拼接）
        goods_ids1 = goods_ids.split(',')
        # 继续判断当前点击的商品id是否存在
        if goods_ids1.count(goods_id) >= 1:
            # 删除当前点击的商品id
            goods_ids1.remove(goods_id)

        # 添加当前点击的商品到浏览记录中第一个位置
        goods_ids1.insert(0,goods_id)
        # 如果超过30条浏览记录就删除最后一条（即最开始添加的）
        if len(goods_ids1) >= 31:
            del goods_ids1[30]

        # 用“, ”拼接成字符串
        goods_ids = ','.join(goods_ids1)
    # 没有浏览记录
    else:
        # 添加当前点击的商品到浏览记录
        goods_ids = goods_id

    # 写入cookie
    response.set_cookie('goods_ids',goods_ids)
    return response

def classify(request,tid,pindex,classify):
    # 根据分类的id查询类型信息
    typeinfo = TypeInfo.objects.get(pk=int(tid))
    # 新品推荐：按id名降序排序，取前2条数据
    news = typeinfo.goodsinfo_set.order_by('-id')[0:2]
    # 当前商品的分类对应的畅销书榜：按点击量（订单数）降序排序，取所有数据
    if classify == '1':
        goods_list = typeinfo.goodsinfo_set.order_by('-gclick').all()
        title = str(typeinfo.ttitle) + '畅销书榜'
    # 当前商品的分类对应的经典书榜：按点击量升序排序，取所有数据
    if classify == '2':
        goods_list = typeinfo.goodsinfo_set.order_by('-gclick').all()
        title = str(typeinfo.ttitle) + '经典书榜'
    # 当前商品的分类对应的特价书榜：按售价升序排序，取所有数据
    if classify == '3':
        goods_list = typeinfo.goodsinfo_set.order_by('gsellprice').all()
        title = str(typeinfo.ttitle) + '特价书榜'
    # 分页：Paginator(列表,int)
    paginator = Paginator(goods_list,10) # 一页放10条数据
    # 显示当前页的数据
    page = paginator.page(int(pindex))
    carts = cart_count(request)
    context = {'title':title,
               'page':page,'paginator':paginator,
               'typeinfo':typeinfo,'news':news,
               'classify':classify,'carts':carts
               }
    return render(request,'cb_goods/classify_list.html',context) # 显示书榜分类页

from haystack.views import SearchView
class MySearchView(SearchView):
    # 重写了extra_context方法
    def extra_context(self):
        # 调用父级SearchView中的extra_context方法
        context = super(MySearchView,self).extra_context()
        # 新增上下文信息
        context['title'] = '搜索'
        context['carts'] = cart_count(self.request)
        return context

