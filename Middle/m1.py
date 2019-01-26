from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse
class Row1(MiddlewareMixin):
    def process_request(self,request):
        print("in 1")
    def process_response(self,request,response):
        print("out 1")
        return response
    def process_view(self,request,view_func,view_func_args,view_func_kwargs):
        print("view 1")


class Row2(MiddlewareMixin):
    def process_request(self,request):
        print("in 2")
        # return HttpResponse("2222")
    def process_response(self,request,response):
        print("out 2 ")
        return response
    def process_view(self,request,view_func,view_func_args,view_func_kwargs):
        print("view 2")


class Row3(MiddlewareMixin):
    def process_request(self,request):
        print("in 3")
    def process_response(self,request,response):
        print("out 3")
        return response
    def process_view(self,request,view_func,view_func_args,view_func_kwargs):
        print("view 3")
    def process_exception(self,request,exception):
        if isinstance(exception,ValueError):
            return HttpResponse("出现异常。。。")
