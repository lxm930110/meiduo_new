from django.contrib.auth.decorators import login_required
from django import http
from django.contrib.auth import mixins

# def my_decorator(view):
#     '''自定义的装饰器:判断是否登录'''
#     def wrapper(request, *args, **kwargs):
#         if request.user.is_authenticated:
#             # 如果用户登录, 则进入这里,正常执行
#             return view(request, *args, **kwargs)
#         else:
#             # 如果用户未登录,则进入这里,返回400的状态码
#             return http.JsonResponse({'code':400,
#                                       'errmsg':'请登录后重试'})
#     return wrapper


# class InfoMixin(object):
#     @classmethod
#     def as_view(cls, **initkwargs):
#
#         view = super().as_view(**initkwargs)
#         return login_required(view)
# from django.views.generic.base import View
#
#
from django.views.generic.base import View


class InfoMixin(mixins.LoginRequiredMixin,View):
    pass