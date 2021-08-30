from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db import transaction
from .models import *
from cb_user import user_decorator
from cb_user.models import UserInfo
from cb_cart.models import *
from datetime import datetime
from decimal import Decimal
import pdb

# Create your views here.
@user_decorator.login
def order(request):
    # 查询用户对象
    user = UserInfo.objects.get(id=request.session['user_id'])
    # 根据提交查询购物车信息
    # pdb.set_trace()
    get = request.GET
    cart_ids = get.getlist('cart_id')
    # cart_ids = request.GET.getlist('cart_id')
    cart_ids1 = [int(item) for item in cart_ids]
    carts = CartInfo.objects.filter(id__in=cart_ids1)
    context = {'title':'提交订单','carts':carts,'user':user,'cart_ids':','.join(cart_ids)}
    return render(request,'cb_order/place_order.html',context)

@user_decorator.login
@transaction.atomic()
def order_handle(request):
    # 保存一个点：回滚的点（回滚点、回退点）
    tran_id = transaction.savepoint()
    # 接收购物车id
    cart_ids = request.POST.get('cart_ids')
    try:
        # 创建订单对象
        order = OrderInfo()
        now = datetime.now()
        uid = request.session['user_id']
        order.oid = '%s%d'%(now.strftime('%Y%m%d%H%M%S'),uid)
        order.user_id = uid
        # 打印订单id
        order.odate = now
        order.ototal = Decimal(request.POST.get('total'))
        order.save()
        # 创建详单对象
        cart_ids1 = [int(item) for item in cart_ids.split(',')]
        for id1 in cart_ids1:
            detail = OrderDetailInfo()
            detail.order = order
            # 查询购物车信息
            cart = CartInfo.objects.get(id=id1)
            # 判断商品库存
            goods = cart.goods
            # 如果库存大于购买数量
            if goods.gkucun >= cart.count:
                # 减少商品库存
                goods.gkucun = cart.goods.gkucun - cart.count
                goods.save()
                # 完善详单信息
                detail.goods_id = goods.id
                detail.price = goods.gsellprice
                detail.count = cart.count
                detail.save()
                # 删除购物车数据
                cart.delete()
            # 如果库存小于购买数量
            else:
                # 所有操作回滚（到回滚点）
                transaction.savepoint_rollback(tran_id)
                return redirect('/cart/')

        # 保存提交（提交保存点）
        transaction.savepoint_commit(tran_id)
    except Exception as e:
        print(e)
        transaction.savepoint_rollback(tran_id)

    return redirect('/user/order/')