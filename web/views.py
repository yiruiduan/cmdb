from django.shortcuts import render,HttpResponse,redirect
from web import models
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.views.decorators.cache import cache_page
import json


# Create your views here.
def auth(func):
    def inner(request,*args,**kwargs):
        request.session.clear_expired()
        if not request.session.get("is_login",None):
            return redirect("/web/login")
        return func(request,*args,**kwargs)
    return inner

# @csrf_exempt
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
    return  HttpResponse("OK")

# @cache_page(10)
def cache(request):
    import time
    ctime=time.time()
    return render(request,'web/cache.html',{'ctime':ctime})

def singals(request):
    # models.UserInfo.objects.create(user_name="yinuo",user_pwd="123456",user_tel="13321123556",user_email="yinuo@163.com")
    print('finish!!!!!')
    from sg import yinuo
    yinuo.send(sender='yiruiduan',top="55",size=66)

    return HttpResponse("on")
from django import forms
class FM(forms.Form):
    user=forms.CharField()
    password=forms.CharField()
    telphone=forms.CharField()
    email=forms.EmailField(error_messages={"invalid":"邮箱格式错误","required":"邮箱不能为空"})

def register(request):
    if request.method == "GET":
        fm_obj=FM()
        return render(request,'web/register.html',{'fm_obj':fm_obj})
    if request.method == 'POST':
        fm_obj=FM(request.POST)
        r1=fm_obj.is_valid()
        print(fm_obj.errors.as_json())

        return render(request,'web/register.html',{'fm_obj':fm_obj})