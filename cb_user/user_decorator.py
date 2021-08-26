from django.shortcuts import redirect
from django.http import HttpResponse,HttpResponseRedirect

# 定义装饰器：之后装饰func指向的函数。如果未登录则转到登录页面：根据session判断
def login(func):
    def login_fun(request,*args,**kwargs): # 之前的请求有一些参数需要传递，所以需要*args、**kwargs接收并继续传递
        # 如果有session的user_id键
        if request.session.has_key('user_id'):
            # 继续执行func函数
            return func(request,*args,**kwargs)
        else:
            red = HttpResponseRedirect('/user/login/')
            # 登录之后返回来登录之前的页面：需要使用request.get_full_path()获取当前请求的包含参数的url完整路径，不能使用url匹配
            red.set_cookie('url',request.get_full_path())
            return red

    return login_fun