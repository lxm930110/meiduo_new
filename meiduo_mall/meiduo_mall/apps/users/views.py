from django.http import JsonResponse

# Create your views here.
from django.views import View

from users.models import User

class RegisterUser(View):
    def post(self,request):

        # 接收请求
        #  验证
        # 处理
        # 验证
        pass

class UserName(View):
    # 验证用户名是否重复
    def get(self, request, username):
        try:
            count = User.objects.filter(username=username).count()
        except Exception as e:
            return JsonResponse({'code': 400, 'errmsg': '数据库错误'})
        return JsonResponse({'code': 400, 'errmsg': '数据库错误', 'count': count})

class Mobile(View):
    # 验证手机号是否重复
    def get(self, request, mobile):
        try:
            count = User.objects.filter(moblie=mobile).count()
        except Exception as e:
            return JsonResponse({'code': 400, 'errmsg': '数据库错误'})
        return JsonResponse({'code': 400, 'errmsg': '数据库错误', 'count': count})


