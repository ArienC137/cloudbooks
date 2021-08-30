from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from .models import *
from cb_star.models import *
from cb_user import user_decorator

# Create your views here.
@user_decorator.login
def cart(request):
    uid = request.session['user_id']
    # 查询当前登录用户的所有购物车信息
    carts = CartInfo.objects.filter(user_id=uid)
    context = {'title':'购物车','carts':carts}
    return render(request,'cb_cart/cart.html',context) # 显示购物车页

@user_decorator.login
def add(request,gid,count): # gid是商品id，count是添加的数量
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
    # 判断是ajax请求（动画形式）直接添加商品到购物车而不是通过链接跳转到购物车
    if request.is_ajax():
        count = CartInfo.objects.filter(user_id=request.session['user_id']).count()
        # 返回当前用户购买的商品数量
        return JsonResponse({'count':count})
    else:
        # 直接转向购物车页面
        return redirect('/cart/')

@user_decorator.login
def edit(request,cart_id,count):
    try:
        cart = CartInfo.objects.get(pk=int(cart_id))
        # 把当前用户购买的商品数量count转换成整型，然后赋值给count属性，再让count1变量指向它
        count1 = cart.count = int(count)
        cart.save()
        data = {'ok':0}
    except Exception as e:
        data = {'ok':count1}

    return JsonResponse(data)

@user_decorator.login
def delete(request,cart_id):
    try:
        cart = CartInfo.objects.get(pk=int(cart_id))
        # 从数据库中删除
        cart.delete()
        data = {'ok':1}
    except Exception as e:
        data = {'ok':0}

    return JsonResponse(data)

@user_decorator.login
def add_star(request,gid,cart_id):
    uid = request.session['user_id']
    gid = int(gid)
    # 查询我的收藏中是否已经有此商品，没有则新增，并从购物车中删除此商品
    stars = StarInfo.objects.filter(user_id=uid,goods_id=gid)
    if len(stars) >= 1:
        # 获取此商品
        star = stars[0]
        # 当前用户收藏的此商品的数量
        count = 1
        state = 'ok'
    else:
        # 新建一个我的收藏对象
        star = StarInfo()
        # 赋值
        star.user_id = uid
        star.goods_id = gid
        count = 0
        cart = CartInfo.objects.get(pk=int(cart_id))
        # 从数据库中删除
        cart.delete()
        state = 'ok'

    star.save()
    # 判断是ajax请求直接添加商品到我的收藏
    if request.is_ajax():
        # 返回当前用户收藏的此商品的数量
        return JsonResponse({'count':count,'state':state})



