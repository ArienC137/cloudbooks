from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.core.paginator import *

# Create your views here.
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
    # 价格
    if sort == '2':
        goods_list = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-gprice')
    # 人气（点击量）
    if sort == '3':
        goods_list = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-gclick')
    # 分页：Paginator(列表,int)
    paginator = Paginator(goods_list,10) # 一页放10条数据
    # 显示当前页的数据
    page = paginator.page(int(pindex))
    context = {'title':typeinfo.ttitle,'page_name':1,
               'page':page,
               'paginator':paginator,
               'typeinfo':typeinfo,
               'sort':sort,
               'news':news,
               'disc':disc
               }
    return render(request,'cb_goods/list.html',context) # 显示列表页

def detail(request,id):
    # 根据id查询商品
    goods = GoodsInfo.objects.get(pk=int(id))
    # 点击量+1
    goods.gclick = goods.gclick+1
    # 当前商品的分类对应的特价书榜：按折扣升序排序，取前4条数据
    goods.gdiscount = goods.gsellprice*10//goods.gprice
    goods.save()
    disc = goods.gtype.goodsinfo_set.order_by('gdiscount')[0:4]
    context = {'title':goods.gtype.ttitle,'page_name':1,'g':goods,'id':id,'page_name':0,'disc':disc}
    return render(request,'cb_goods/detail.html',context) # 显示详情页

def classify(request,tid,pindex,classify):
    # 根据分类的id查询类型信息
    typeinfo = TypeInfo.objects.get(pk=int(tid))
    # 新品推荐：按id名降序排序，取前2条数据
    news = typeinfo.goodsinfo_set.order_by('-id')[0:2]
    # 当前商品的分类对应的畅销书榜：按点击量（订单数）降序排序，取所有数据
    if classify == '1':
        goods_list = typeinfo.goodsinfo_set.order_by('-gclick').all()
    # 当前商品的分类对应的经典书榜：按点击量升序排序，取所有数据
    if classify == '2':
        goods_list = typeinfo.goodsinfo_set.order_by('-gclick').all()
    # 当前商品的分类对应的特价书榜：按售价升序排序，取所有数据
    if classify == '3':
        goods_list = typeinfo.goodsinfo_set.order_by('gsellprice').all()
    # 分页：Paginator(列表,int)
    paginator = Paginator(goods_list,10) # 一页放10条数据
    # 显示当前页的数据
    page = paginator.page(int(pindex))
    context = {'title':typeinfo.ttitle,'page_name':1,
               'page':page,
               'paginator':paginator,
               'typeinfo':typeinfo,
               'news':news,
               'classify':classify
               }
    return render(request,'cb_goods/classify_list.html',context) # 显示书榜分类页

