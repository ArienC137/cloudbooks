from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from .models import *
from cb_cart.models import *
from cb_user import user_decorator
from django.core.paginator import *
from django.contrib import messages

# Create your views here.
@user_decorator.login
def star(request,pindex):
    uid = request.session['user_id']
    # 查询当前登录用户的所有收藏信息
    stars = StarInfo.objects.filter(user_id=uid)
    # 查询当前登录用户的所有购物车信息
    carts = CartInfo.objects.filter(user_id=uid)
    goods_list = StarInfo.objects.order_by('-sdate')
    # 分页：Paginator(列表,int)
    paginator = Paginator(goods_list,10) # 一页放10条数据
    # 显示当前页的数据
    page = paginator.page(int(pindex))
    context = {'title':'我的收藏','page_name':2,
               'stars':stars,'carts':carts,
               'paginator':paginator,'page':page}
    return render(request,'cb_user/user_center_star.html',context)

@user_decorator.login
def add(request,gid):
    uid = request.session['user_id']
    gid = int(gid)
    # 查询我的收藏中是否已经有此商品，没有则新增
    stars = StarInfo.objects.filter(user_id=uid,goods_id=gid)
    if len(stars) >= 1:
        # 获取此商品
        star = stars[0]
        # 当前用户收藏的此商品的数量
        count = 1
    else:
        # 新建一个我的收藏对象
        star = StarInfo()
        # 赋值
        star.user_id = uid
        star.goods_id = gid
        count = 0

    star.save()
    # 判断是ajax请求直接添加商品到我的收藏而不是通过链接跳转到我的收藏
    if request.is_ajax():
        # 返回当前用户收藏的此商品的数量
        return JsonResponse({'count':count})
    else:
        # 直接转向我的收藏页面
        return redirect('/star/1/')

@user_decorator.login
def delete(request,star_id):
    try:
        star = StarInfo.objects.get(pk=int(star_id))
        # 从数据库中删除
        star.delete()
        data = {'ok':1}
    except Exception as e:
        data = {'ok':0}

    return JsonResponse(data)

@user_decorator.login
def add_cart(request,gid,count):
    # messages.success(request,'count')
    uid = request.session['user_id']
    gid = int(gid)
    count = int(count)
    # 查询购物车中是否已经有此商品，有则数量增加，没有则新增
    carts = CartInfo.objects.filter(user_id=uid,goods_id=gid)
    if len(carts) >= 1:
        # 获取此商品
        cart = carts[0]
        # 数量增加
        cart.count = cart.count + count
    else:
        # 新建一个购物车对象
        cart = CartInfo()
        # 赋值
        cart.user_id = uid
        cart.goods_id = gid
        cart.count = count

    cart.save()
    # 判断是ajax请求直接添加商品到购物车而不是通过链接跳转到购物车
    if request.is_ajax():
        return JsonResponse({'count':count})
    else:
        # 直接转向购物车页面
        return redirect('/cart/')