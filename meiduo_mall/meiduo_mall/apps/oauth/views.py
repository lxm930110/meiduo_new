from django.conf import settings
from django.contrib.auth import login
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django_redis import get_redis_connection

from carts.merge_carts_utils import mergey_carts
from meiduo_mall.utils.meiduo_signature import loads, dumps

from django.views.generic.base import View
from QQLoginTool.QQtool import OAuthQQ

from oauth.models import OAuthQQUser
import re, logging, json

logger = logging.getLogger('django')

from users.models import User


class QQURLView(View):
    def get(self, request):
        next = request.GET.get('next')
        # 实例化
        oauthqq = OAuthQQ(client_id=settings.QQ_CLIENT_ID,
                          client_secret=settings.QQ_CLIENT_SECRET,
                          redirect_uri=settings.QQ_REDIRECT_URI,
                          state=next, )
        # 获取qq授权登录地址
        qq_login_url = oauthqq.get_qq_url()

        return JsonResponse({'code': 0, 'errmsg': 'OK', 'login_url': qq_login_url})


class QQLoginView(View):

    def get(self, request):

        # 获取qq服务器返回的code
        code = request.GET.get('code')
        # 判断code是否过期
        if not code:
            return JsonResponse({'code': 400, 'errmsg': 'code已过期'})
        # 实例化
        oauthqq = OAuthQQ(client_id=settings.QQ_CLIENT_ID,
                          client_secret=settings.QQ_CLIENT_SECRET,
                          redirect_uri=settings.QQ_REDIRECT_URI, )
        try:
            # 根据code获取token
            token = oauthqq.get_access_token(code)
            # 根据token获取openid
            openid = oauthqq.get_open_id(token)
        except Exception as e:

            logger.error(e)

            return JsonResponse({'code': 400, 'errmsg': '获取openid失败'})

        # 判断openid在表中是否存在
        try:
            qquser = OAuthQQUser.objects.get(openid=openid)

        except:
            # 不存在
            # 给openid进行加密处理
            data = {'openid': openid}
            token_str = dumps(data, 60*10)

            return JsonResponse({'code': 302, 'errmsg': '跳转到登录页面', 'access_token': token_str})
        else:
            # 存在
            user = qquser.user
            # 状态保持
            login(request, user)
            response = JsonResponse({'code': 0, 'errmsg': 'OK'})
            # 登录状态保持后合并购物车
            response = mergey_carts(request, response)
            # 设置cookie,把用户名写入
            response.set_cookie('username', user.username, max_age=60 * 60 * 24 * 14)
            return response

    def post(self, request):
        # 接受参数
        dict = json.loads(request.body.decode())
        access_token = dict.get('access_token')
        mobile = dict.get('mobile')
        password = dict.get('password')
        msg_code = dict.get('sms_code')

        # 校验参数
        # 判断参数是否齐全
        if not all([mobile, password, msg_code]):
            return JsonResponse({'code': 400,
                                 'errmsg': '缺少必传参数'})

        # 判断手机号是否合法
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return JsonResponse({'code': 400,
                                 'errmsg': '请输入正确的手机号码'})

        # 判断密码是否合格
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return JsonResponse({'code': 400,
                                 'errmsg': '请输入8-20位的密码'})

        # 判断短信验证码是否一致
        # 创建 redis 链接对
        redis_conn = get_redis_connection('msg_code')

        # 从 redis 中获取 sms_code 值
        msg_code_server = redis_conn.get(mobile)

        # 判断是否存在
        if msg_code_server is None:
            # 如果没有, 直接返回:
            return JsonResponse({'code': 400,

                                 'errmsg': '短信验证码失效'})
        # 判断验证码是否一致
        if msg_code != msg_code_server.decode():
            # 如果不匹配, 则直接返回:
            return JsonResponse({'code': 400,
                                 'errmsg': '短信验证码不一致'})

        # 解码获取openid
        openid_dict = loads(access_token, 60*10)
        openid = openid_dict.get('openid')
        print(openid)
        if not openid:
            return JsonResponse({'code': 400,
                                 'errmsg': 'openid过期'})

        try:
            user = User.objects.get(mobile=mobile)

        except:
            # 新建用户
            user = User.objects.create_user(mobile,
                                            password=password,
                                            mobile=mobile)
        else:
            # 验证密码
            if not user.check_password(password):
                return JsonResponse({'code': 400,
                                     'errmsg': '输入的密码不正确'})
            # 绑定 openid
        try:
            OAuthQQUser.objects.create(openid=openid,
                                       user=user)
        except:
            return JsonResponse({'code': 400,
                                 'errmsg': '往数据库添加数据出错'})
            # 状态保持
        login(request, user)

        # 响应:
        response = JsonResponse({'code': 0,
                                 'errmsg': 'ok'})
        # 登录状态保持后合并购物车
        response = mergey_carts(request, response)

        #  设置用户名写入cookie，
        response.set_cookie('username',
                            user.username,
                            max_age=3600 * 24 * 14)

        return response


    # 再写一遍

class QQloginView1(View):
    def get(self, request):
        code = request.GET.get('code')
        if not code:
            return JsonResponse({'code': 400, 'errmsg': 'code已过期'})
        oauthqq = OAuthQQ(
            client_id=settings.QQ_CLIENT_ID,
            client_secret=settings.QQ_CLIENT_SECRET,
            redirect_uri=settings.QQ_REDIRECT_URI,)
        try:
            token = oauthqq.get_access_token(code)
            openid = oauthqq.get_open_id(token)
        except:
            return JsonResponse({'code': 400, 'errmsg': '获取openid失败'})
        try:
            qq_object = OAuthQQUser.objects.get(openid=openid)
        except:
            data = {'openid':openid}
            access_token = dumps(data,60*10)
            return JsonResponse({'code':'302','errmsg':'OK','access_token':access_token})
        else:
            user = qq_object.user
            login(request, user)
            response = JsonResponse({'code':0,'errmsg':'OK'})
            response.set_cookie('username', user.username, max_age=60 * 60 * 24 * 14)
            return response


    def post(self,request):
        dict = json.loads(request.body.decode())
        access_token = dict.get('access_token')
        mobile = dict.get('mobile')
        password = dict.get('password')
        msg_code = dict.get('sms_code')
        if not all([access_token,mobile,password,msg_code]):
            return JsonResponse({'code': 400, 'errmsg': '参数不完整'})

        # 判断短信验证码是否一致
        # 创建 redis 链接对
        redis_conn = get_redis_connection('msg_code')

        # 从 redis 中获取 sms_code 值
        msg_code_server = redis_conn.get(mobile)

        # 判断是否存在
        if msg_code_server is None:
            # 如果没有, 直接返回:
            return JsonResponse({'code': 400,
                                 'errmsg': '短信验证码失效'})
        # 判断验证码是否一致
        if msg_code != msg_code_server.decode():
            # 如果不匹配, 则直接返回:
            return JsonResponse({'code': 400,
                                 'errmsg': '短信验证码不一致'})
        dict_openid = dumps(access_token, 60*10)
        # 获取openis
        openid = dict_openid.get('openid')
        if not openid:
            return JsonResponse({'code': 400,
                                 'errmsg': 'openid过期'})
        try:
            user = User.objects.get(mobile=mobile)
        except:
            try:
                user = User.objects.create_user(mobile,mobile=mobile,
                                         password=password)
            except:
                return JsonResponse({'code': 400,
                                     'errmsg': '数据库错误'})
        else:
            if not user.check_password(password):
                return JsonResponse({'code': 400,
                                     'errmsg': '密码错误'})
        try:
            OAuthQQUser.objects.create(openid=openid, user=user)
        except:
            return JsonResponse({'code': 400,
                                 'errmsg': '数据库错误'})
        login(request, user)
        response = JsonResponse({'code': 0, 'errmsg': 'OK'})
        response.set_cookie('username', user.username, max_age=60 * 60 * 24 * 14)
        return response










