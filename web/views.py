from django.shortcuts import render,HttpResponse,redirect
from web import models
import json
# Create your views here.
def auth(func):
    def inner(request,*args,**kwargs):
        request.session.clear_expired()
        print(request.session.get('is_login'))
        if not request.session.get("is_login",None):
            return redirect("/web/login")
        return func(request,*args,**kwargs)
    return inner

def login(request):
    if request.method == "GET":
        return render(request,"web/login.html")
    elif request.method == "POST":
        u=request.POST.get("user",None)
        p=request.POST.get("password",None)
        print(u,p)
        if  models.UserInfo.objects.filter(user_name=u,user_pwd=p):
            # 生成随机字符串
            # 写到用户浏览器cookie
            # 保存到session中
            # 在随机字符串对应的字典中设置相关内容
            request.session['username']=u
            request.session['is_login']=True
            request.session.set_expiry(60*60)
            return redirect("/web/index")
        else:
            return  render(request,"web/login.html",{"error_msg":"用户名密码错误"})


def loginout(request):
    request.session.clear()
    return redirect("/web/login")
@auth
def index(request):
    return render(request,"web/host_manager.html")

@auth
def test(request):
    return  HttpResponse("test")