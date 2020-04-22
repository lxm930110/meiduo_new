from django.contrib.auth import login
from django.http import JsonResponse
from django.views import View
from django_redis import get_redis_connection
import re
from users.models import User
import json


class RegisterUserView(View):
    def post(self,request):
        # 接收请求
        dict = json.loads(request.body.decode())
        username = dict.get('username')
        password = dict.get('password')
        password2 = dict.get('password2')
        mobile = dict.get('mobile')
        allow = dict.get('allow')
        msg_code_sro = dict.get('sms_code')

        # 验证参数完整性
        if not all([username, password, password2, mobile, allow, msg_code_sro]):
            return JsonResponse({'code': 400,'errmsg': '参数不完整'})

        # 用户名验证
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return JsonResponse({'code': 400,'errmsg': 'username格式有误'})

        # 密码验证
        if not re.match(r'^[a-zA-Z0-9]{8,20}$', password):
            return JsonResponse({'code': 400,'errmsg': 'password格式有误'})

        # 确认密码不一致性
        if password != password2:
            return JsonResponse({'code': 400,'errmsg': '密码不一致性'})
        # 手机号验证
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return JsonResponse({'code': 400,'errmsg': '手机格式有误'})
        # allow验证
        if allow != True:
            return JsonResponse({'code': 400,'errmsg': 'allow格式有误'})

        # 短信验证 (链接redis)
        msg_redis_cli = get_redis_connection('msg_code')

        # 从redis中取值
        msg_code = msg_redis_cli.get(mobile)

        # 判断该值是否存在
        if not msg_code:
            return JsonResponse({'code': 400, 'errmsg': '短信验证码已过期'})
        # 短信验证码对比
        if msg_code_sro != msg_code.decode():
            return JsonResponse({'code': 400, 'errmsg': '短信验证码有误'})

        # 保存到数据库 (username password mobile)
        try:
            # 使用create_user方法可以给密码加密处理
            user = User.objects.create_user(username=username,
                                            password=password,
                                            mobile=mobile)
        except Exception as e:
            return JsonResponse({'code': 400, 'errmsg': '保存到数据库出错'})
        # 保持会话状态
        login(request,user)

        # 响应
        return JsonResponse({'code': 0, 'errmsg': 'ok'})


class UserNameView(View):
    # 验证用户名是否重复
    def get(self, request, username):
        try:
            count = User.objects.filter(username=username).count()
        except Exception as e:
            return JsonResponse({'code': 400, 'errmsg': '数据库错误'})
        return JsonResponse({'code': 400, 'errmsg': '数据库错误', 'count': count})


class MobileView(View):
    # 验证手机号是否重复
    def get(self, request, mobile):
        try:
            count = User.objects.filter(moblie=mobile).count()
        except Exception as e:
            return JsonResponse({'code': 400, 'errmsg': '数据库错误'})
        return JsonResponse({'code': 400, 'errmsg': '数据库错误', 'count': count})


