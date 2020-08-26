
from django.contrib.auth.backends import ModelBackend
from users.models import User


class MeiduoModelBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):

        if request is None:
            # 管理员用户
            try:
                # 判断是否是用户名登录
                user = User.objects.get(username=username,is_active=True,is_superuser=True)
            except:
                return None
            # 判断密码
            if user.check_password(password):
                return user
            else:
                return None

            # 普通用户
        else:
            try:
                # 判断是否是用户名登录
                user = User.objects.get(username=username)
            except:
                try:
                    # 判断是否是手机号登录
                    user = User.objects.get(mobile=username)
                except:
                    return None
            # 判断密码
            if user.check_password(password):
                return user
            else:
                return None







