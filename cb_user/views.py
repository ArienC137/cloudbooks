from django.shortcuts import render,redirect # redirect重定向
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from .models import *
from cb_goods.models import *
from hashlib import sha1
import random

# Create your views here.
def index(request):
    return render(request,'cb_user/index.html') # 显示首页（logo页）

def register(request):
    return render(request,'cb_user/register.html') # 显示注册页面

def register_handle(request):
    # 接收用户输入
    post = request.POST
    # user_name、pwd、cpwd和email都是register.html文件中name属性的值
    uname = post.get('user_name')
    upwd = post.get('pwd')
    upwd2 = post.get('cpwd')
    uemail = post.get('email')
    # 判断两次密码是否一致（虽然js已经验证过一次，但最好再验证一次）
    if upwd != upwd2:
        # 返回注册页面，同时函数结束
        return redirect('/user/register/')
    # 密码加密
    s1 = sha1()
    # 必须指定要加密的字符串的字符编码格式为utf8，否则报错：python3中的字符是unicode对象，不能直接加密
    s1.update(upwd.encode("utf8"))
    upwd3 = s1.hexdigest()
    # 创建对象（从而通过模型类和数据库交互）
    user = UserInfo()
    # 给属性赋值
    user.uname = uname
    user.upwd = upwd3
    user.uemail = uemail
    # 保存到数据库中
    user.save()
    # 注册成功，转到登录页面
    return redirect('/user/login/')

def register_exist(request):
    # 用get方法根据键接收值
    uname = request.GET.get('uname')
    # 根据接收值查询匹配的数据的个数
    count = UserInfo.objects.filter(uname=uname).count()
    return JsonResponse({'count':count})

def login(request):
    # 获取COOKIES的值
    uname = request.COOKIES.get('uname','')
    # 把title、error_name、error_pwd和uname变量的值传给模板：error_name和error_pwd必须写，否则在login.html中的js会报错
    context = {'title':'用户登录','error_name':0,'error_pwd':0,'uname':uname}
    return render(request,'cb_user/login.html',context) # 显示登录页面

def login_handle(request):
    # 接收请求信息
    post = request.POST
    # username、pwd和jizhu都是login.html文件中name属性的值
    uname = post.get('username')
    upwd = post.get('pwd')
    # get('键',default=None)方法：设置value属性的值默认值为0即没有选中选框。则选中选框时'jizhu'键的值为1，没有选中选框时也就不存在'jizhu'键，返回值为0
    jizhu = post.get('jizhu',0)
    # 根据用户名查询对象
    # 使用filter而不使用get的原因：如果未找到，get会产生异常
    users = UserInfo.objects.filter(uname=uname)
    # 查到用户名时：判断密码是否正确，正确则跳转到商品首页
    if len(users) == 1:
        # 密码加密
        s1 = sha1()
        s1.update(upwd.encode("utf8"))
        # users[0]：使用filter得到的列表中的第一个元素即用户名（对象）。users[0].upwd：获取用户名对象的upwd属性的值
        if s1.hexdigest() == users[0].upwd:
            # 不使用redirect而使用HttpResponseRedirect的原因：redirect不能设置cookie信息
            red = HttpResponseRedirect('/user/index_list/')
            # 记住用户名（实际操作是存到cookie里）：设置cookie
            if jizhu != 0:
                red.set_cookie('uname',uname)
            else:
                # 设置cookie的值为空
                red.set_cookie('uname','',max_age=-1)
            # 设置session
            # 存储用户名的id，以后查找用户名时可以根据id查找
            request.session['user_id'] = users[0].id
            # 存储用户名，因为很多页面需要显示用户名（使用频率高），每次都根据id查找效率低
            request.session['user_name'] = uname
            # 返回用户中心页面
            return red
        else:
            context = {'title':'用户登录','error_name':0,'error_pwd':1,'uname':uname,'upwd':upwd}
            return render(request,'cb_user/login.html',context) # 显示登录页面
    # 未查到用户名时
    else:
        # 把title、error_name、error_pwd、uname和upwd变量的值传给模板
        # error_name和error_pwd变量传给login.html中的js：error_name的值为1即用户名错误，error_pwd的值为0即密码正确。uname和upwd的值是当前的用户名和密码
        context = {'title':'用户登录','error_name':1,'error_pwd':0,'uname':uname,'upwd':upwd}
        return render(request,'cb_user/login.html',context) # 显示登录页面

def index_list(request):
    # 默认随机查询一个商品分类的最新的2条（按id）、最热的10条数据（按gclick）
    typelist = TypeInfo.objects.all()
    t = random.randint(0,len(typelist)-1)
    type0 = typelist[t].goodsinfo_set.order_by('-id')[0:2]
    type01 = typelist[t].goodsinfo_set.order_by('-gclick')[0:10]
    context = {'title':'首页','page_name':1,
               'type0':type0,'type01':type01,
               'type':typelist[t]
               } # 把page_name变量的值1传给模板是为了判断顶部栏与用户中心页面的区别，从而显示与用户中心页面不同的部分
    return render(request,'cb_goods/index_list.html',context) # 显示商品首页

def info(request):
    user_email = UserInfo.objects.get(id=request.session['user_id']).uemail
    # 数据库中的uaddress和uphone字段的默认值是''，所以不会报错
    user_address = UserInfo.objects.get(id=request.session['user_id']).uaddress
    user_phone = UserInfo.objects.get(id=request.session['user_id']).uphone
    context = {'title':'用户中心','user_email':user_email,'user_name':request.session['user_name'],'user_address':user_address,'user_phone':user_phone,'page_name':2}
    return render(request,'cb_user/user_center_info.html',context) # 显示用户中心页面

def order(request):
    context = {'title':'用户中心','page_name':2}
    return render(request,'cb_user/user_center_order.html',context) # 显示用户订单页面

def site(request):
    # 点击（超）链接的请求方式是GET
    # 用户已经登录，所以查找用户名时可以根据id查找
    user = UserInfo.objects.get(id=request.session['user_id'])
    # form表单提交到当前页面时，视图接收的请求方式变为POST
    if request.method == 'POST':
        # 接收用户输入并给属性赋值
        post = request.POST
        user.ushou = post.get('ushou')
        user.uaddress = post.get('uaddress')
        user.uyoubian = post.get('uyoubian')
        user.uphone = post.get('uphone')
        # 保存到数据库中
        user.save()
    context = {'title':'用户中心','user':user,'page_name':2}
    return render(request,'cb_user/user_center_site.html',context) # 显示用户地址页面

