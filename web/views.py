from django.shortcuts import render,HttpResponse,redirect
from web import models
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.views.decorators.cache import cache_page
import json
from sg import cmdb_log

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
    print('finish!!!!!')
    # from sg import cmdb_log
    # cmdb_log.send(sender='yiruiduan',top="55",size=66)
    return HttpResponse("on")

from django.forms import Form
from django.forms import widgets
from django.forms import fields
from django.core.validators import RegexValidator
class FM(Form):

    user_name=fields.CharField(
        required=True,
        widget=widgets.TextInput(attrs={'placeholder': '用户名'}),
    )
    user_pwd=fields.CharField(
        required=True,
        widget=widgets.TextInput(attrs={'placeholder': '密码'}),
                             )
    user_tel=fields.CharField(
        required=True,
        validators=[RegexValidator(r'^[0-9]+$', '请输入数字'), RegexValidator(r'^1([38]\d|5[0-35-9]|7[3678])\d{8}$', '请输入正确的手机号码')],
        widget=widgets.TextInput(attrs={'placeholder': '手机号'}),
    )
    user_email=fields.EmailField(
        required=True,
        widget=widgets.TextInput(attrs={'placeholder': '邮箱'}),
        error_messages={"invalid":"邮箱格式错误","required":"邮箱不能为空"}
    )

def register(request):
    if request.method == "GET":
        fm_obj=FM()
        return render(request,'web/register.html',{'fm_obj':fm_obj})
    if request.method == 'POST':
        fm_obj=FM(request.POST)
        r1=fm_obj.is_valid()
        if r1:
            from  django.db import connection
            models.UserInfo.objects.create(**fm_obj.cleaned_data)
            print(connection.queries[-1])
            cmdb_log.send(sender="yiruiduan",sql=connection.queries[-1])
        else:
            print(fm_obj.errors.as_json())

        return render(request,'web/register.html',{'fm_obj':fm_obj})