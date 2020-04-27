from django.conf import settings
from django.contrib.auth import login, logout, authenticate
from django.http import JsonResponse
from django.views import View
from django_redis import get_redis_connection
import re
from users.models import User, Address
import json, logging

logger = logging.getLogger('django')
from meiduo_mall.utils.info import InfoMixin
from django.shortcuts import redirect

from meiduo_mall.utils.meiduo_signature import dumps, loads
from celery_tasks.email.tasks import send_verify_email


class RegisterUserView(View):
    def post(self, request):
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
            return JsonResponse({'code': 400, 'errmsg': '参数不完整'})

        # 用户名验证
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return JsonResponse({'code': 400, 'errmsg': 'username格式有误'})

        # 密码验证
        if not re.match(r'^[a-zA-Z0-9]{8,20}$', password):
            return JsonResponse({'code': 400, 'errmsg': 'password格式有误'})

        # 确认密码不一致性
        if password != password2:
            return JsonResponse({'code': 400, 'errmsg': '密码不一致性'})
        # 手机号验证
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return JsonResponse({'code': 400, 'errmsg': '手机格式有误'})
        # allow验证
        if allow != True:
            return JsonResponse({'code': 400, 'errmsg': 'allow格式有误'})

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
        login(request, user)

        # 响应
        response = JsonResponse({'code': 0, 'errmsg': 'OK'})

        response.set_cookie('username', username, max_age=60 * 60 * 24 * 14)

        return response


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


class LoginView(View):
    def post(self, request):
        dict = json.loads(request.body.decode())
        username = dict.get('username')
        password = dict.get('password')
        remembered = dict.get('remembered')
        if not all([username, password, remembered]):
            return JsonResponse({'code': 400, 'errmsg': '参数不完整'})
        user = authenticate(request, username=username, password=password)
        if user is None:
            return JsonResponse({'code': '400', 'errmsg': '用户名或者密码不正确'})
        # 状态保持
        login(request, user)

        if remembered != True:

            request.session.set_expiry(0)
        else:
            request.session.set_expiry(None)

        response = JsonResponse({'code': 0, 'errmsg': 'OK'})

        response.set_cookie('username', username, max_age=60 * 60 * 24 * 14)

        return response


class LogoutView(View):

    def delete(self, requset):
        # 断开会话状态
        logout(requset)
        response = JsonResponse({'code': 0, 'errmsg': 'OK'})
        # 删除保存在cookie里的用户信息
        response.delete_cookie('username')
        return response


class UserCenterInfoView(InfoMixin, View):
    def get(self, request):
        # pass
        # pass
        # this.username = response.data.info_data.username;
        # this.mobile = response.data.info_data.mobile;
        # this.email = response.data.info_data.email;
        # this.email_active = response.data.info_data.email_active;

        info_data = {
            'username': request.user.username,
            'mobile': request.user.mobile,
            'email': request.user.email,
            'email_active': request.user.email_active,
        }
        return JsonResponse({'code': 0, 'errmsg': 'OK', 'info_data': info_data})


class EmailView(InfoMixin, View):

    def put(self, request):
        dict = json.loads(request.body.decode())
        email = dict.get('email')
        # 判断是否eamil存在
        if not email:
            return JsonResponse({'code': 400, 'errmsg': 'email参数不存在'})
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return JsonResponse({'code': 400, 'errmsg': 'email格式错误'})
        try:
            # 修改用户email信息
            request.user.email = email
            request.user.save()
        except Exception as e:
            logger.error(e)
            return JsonResponse({'code': 400, 'errmsg': '保存邮箱错误'})
        data = {'user_id': request.user.id}
        # 对user_id进行加密处理
        user_msg = dumps(data, 60 * 60 * 2)
        # 字符串拼接加密后的路径
        verify_url = settings.EMAIL_VERIFY_URL + user_msg
        # 执行异步发送邮件
        send_verify_email.delay(email, verify_url)

        return JsonResponse({'code': 0, 'errmsg': 'OK'})


class VerifyEmailView(View):
    def put(self, request):
        # 获取token
        token = request.GET.get('token')
        if not token:
            return JsonResponse({'code': 400, 'errmsg': '参数不存在'})
        # 解密获取存user_id（dict格式）
        data_dict = loads(token, 60 * 60 * 2)
        # 在字典中取出user_id
        user_id = data_dict.get('user_id')
        try:
            user = User.objects.get(pk=user_id)
        except Exception as e:
            logger.error(e)
            return JsonResponse({'code': 400, 'errmsg': '数据库出错'})
        # 修改email_active值
        user.email_active = True
        user.save()
        return JsonResponse({'code': 0, 'errmsg': 'OK'})


class CreateAddressView(InfoMixin, View):
    # 增加地址
    def post(self, request):
        # 获取地址总个数:
        try:
            count = Address.objects.filter(user=request.user,
                                           is_deleted=False).count()
        except:
            return JsonResponse({'code': 400,
                                 'errmsg': '获取地址出错'})
            # 判断是否超过上限20个
        if count >= 20:
            return JsonResponse({'code': 400,
                                 'errmsg': '超过地址个数上限'})
        # 接收参数
        dict = json.loads(request.body.decode())
        receiver = dict.get('receiver')
        province_id = dict.get('province_id')
        city_id = dict.get('city_id')
        district_id = dict.get('district_id')
        place = dict.get('place')
        mobile = dict.get('mobile')
        tel = dict.get('tel')
        email = dict.get('email')

        # 集体验证参数
        if not all([receiver, province_id, city_id, district_id, place, mobile]):
            return JsonResponse({'code': 400,
                                 'errmsg': '缺少参数'})

        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return JsonResponse({'code': 400,
                                 'errmsg': '手机格式错误'})
        if tel:
            if not re.match(r'^(0[0-9]{2,3}-)?([2-9][0-9]{6,7})+(-[0-9]{1,4})?$', tel):
                return JsonResponse({'code': 400,
                                     'errmsg': '电话格式错误'})
        if email:
            if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
                return JsonResponse({'code': 400,
                                     'errmsg': '邮箱格式错误'})
        # 保存地址信息
        try:
            address = Address.objects.create(
                user=request.user,
                title=receiver,
                receiver=receiver,
                province_id=province_id,
                city_id=city_id,
                district_id=district_id,
                place=place,
                mobile=mobile,
                tel=tel,
                email=email
            )

            # 设置默认地址
            if not request.user.default_address:
                request.user.default_address = address
                request.user.save()

        except Exception as e:
            logger.error(e)
            return JsonResponse({'code': 400,
                                 'errmsg': '新增地址失败'})
        address_dict = {
            "id": address.id,
            "title": address.title,
            "receiver": address.receiver,
            "province": address.province.name,
            "city": address.city.name,
            "district": address.district.name,
            "place": address.place,
            "mobile": address.mobile,
            "tel": address.tel,
            "email": address.email
        }

        # 响应保存结果
        return JsonResponse({'code': 0,
                             'errmsg': '新增地址成功',
                             'address': address_dict})


class ShowAddressView(InfoMixin, View):
    def get(self, request):
        # 获取所有未删除的地址:
        addresses = Address.objects.filter(user=request.user,
                                           is_deleted=False)
        address_list = []
        # 遍历所有地址
        for address in addresses:
            address_dict = {
                "id": address.id,
                "title": address.title,
                "receiver": address.receiver,
                "province": address.province.name,
                "city": address.city.name,
                "district": address.district.name,
                "place": address.place,
                "mobile": address.mobile,
                "tel": address.tel,
                "email": address.email
            }

            # 把默认地址最先展示
            default_address = request.user.default_address
            if default_address.id == address.id:
                address_list.insert(0, address_dict)
            else:
                address_list.append(address_dict)

        default_id = request.user.default_address_id

        return JsonResponse({'code': 0,
                             'errmsg': 'ok',
                             'addresses': address_list,
                             'default_address_id': default_id})


class UpdateAddressView(InfoMixin, View):
    # 修改地址
    def put(self, request, address_id):
        # 接收参数
        json_dict = json.loads(request.body.decode())
        receiver = json_dict.get('receiver')
        province_id = json_dict.get('province_id')
        city_id = json_dict.get('city_id')
        district_id = json_dict.get('district_id')
        place = json_dict.get('place')
        mobile = json_dict.get('mobile')
        tel = json_dict.get('tel')
        email = json_dict.get('email')

        # 验证参数
        # 集体验证
        if not all([receiver, province_id, city_id, district_id, place, mobile]):
            return JsonResponse({'code': 400, 'errmsg': '缺少参数'})
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return JsonResponse({'code': 400, 'errmsg': '手机格式错误'})
        if tel:
            if not re.match(r'^(0[0-9]{2,3}-)?([2-9][0-9]{6,7})+(-[0-9]{1,4})?$', tel):
                return JsonResponse({'code': 400, 'errmsg': '电话格式错误'})
        if email:
            if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
                return JsonResponse({'code': 400, 'errmsg': '邮箱格式错误'})

        # 修改地址数据
        try:
            Address.objects.filter(pk=address_id).update(
                user=request.user,
                title=receiver,
                receiver=receiver,
                province_id=province_id,
                city_id=city_id,
                district_id=district_id,
                place=place,
                mobile=mobile,
                tel=tel,
                email=email
            )
        except Exception as e:
            logger.error(e)
            return JsonResponse({'code': 400,'errmsg': '修改地址失败'})

        address = Address.objects.get(pk=address_id)
        address_dict = {
            "id": address.id,
            "title": address.title,
            "receiver": address.receiver,
            "province": address.province.name,
            "city": address.city.name,
            "district": address.district.name,
            "place": address.place,
            "mobile": address.mobile,
            "tel": address.tel,
            "email": address.email
        }

        # 响应
        return JsonResponse({'code': 0, 'errmsg': '修改地址成功', 'address': address_dict})

    def delete(self, request, address_id):
        # 删除地址
        try:
            address = Address.objects.get(id=address_id)
            address.is_deleted = True
            address.save()
        except Exception as e:
            logger.error(e)
            return JsonResponse({'code': 400, 'errmsg': '删除地址失败'})
        # 响应
        return JsonResponse({'code': 0, 'errmsg': '删除地址成功'})


class DefaultAddressView(View):
    # 设置默认地址
    def put(self, request, address_id):
        try:
            address = Address.objects.get(id=address_id)
            request.user.default_address_id = address.id
            request.user.save()
        except Exception as e:
            logger.error(e)
            return JsonResponse({'code': 400, 'errmsg': '设置默认地址失败'})
        return JsonResponse({'code': 0,  'errmsg': '设置默认地址成功'})


class UpdateTitleAddressView(View):
    # 设置地址的标题
    def put(self, request, address_id):
        json_dict = json.loads(request.body.decode())
        title = json_dict.get('title')
        try:
            address = Address.objects.get(pk=address_id)
            address.title = title
            address.save()
        except Exception as e:
            logger.error(e)
            return JsonResponse({'code': 400, 'errmsg': '设置地址标题失败'})
        # 响应
        return JsonResponse({'code': 0, 'errmsg': '设置地址标题成功'})


class ModifyPasswordView(InfoMixin, View):
    # 修改密码
    def put(self, request):
        # 接收参数
        dict = json.loads(request.body.decode())
        old_password = dict.get('old_password')
        new_password = dict.get('new_password')
        new_password2 = dict.get('new_password2')

        # 参数集体验证
        if not all([old_password, new_password, new_password2]):
           return JsonResponse({'code':400,'errmsg':'缺少参数'})

        result = request.user.check_password(old_password)
        if not result:
            return JsonResponse({'code':400,'errmsg':'原密码错误'})
        if not re.match(r'^[0-9A-Za-z]{8,20}$', new_password):
            return JsonResponse({'code':400,'errmsg':'密码格式错误'})
        if new_password != new_password2:
            return JsonResponse({'code':400,'errmsg':'密码不一致'})
        # 修改密码
        try:
            # 保存新密码并加密
            request.user.set_password(new_password)
            request.user.save()
        except Exception as e:
            logger.error(e)
            return JsonResponse({'code':400, 'errmsg':'修改密码失败'})
        logout(request)
        response = JsonResponse({'code':0, 'errmsg':'ok'})
        response.delete_cookie('username')
        # 响应
        return response