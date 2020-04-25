from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View

from django_redis import get_redis_connection

from meiduo_mall.libs.captcha.captcha import captcha
from random import randint

from meiduo_mall.libs.yuntongxun.sms import CCP

from celery_tasks.sms.tasks import ccp_send_sms_code


class ImageCode(View):
    # 生成图形验证码
    def get(self, request, uuid):
        # 通过调用generate_captcha()方法获取图像验证码
        name, text, image = captcha.generate_captcha()
        redis_cli = get_redis_connection('image_code')
        redis_cli.setex(uuid, 60 * 5, text)
        return HttpResponse(image, content_type='image/jpg')


class MsgCodeView(View):
    def get(self, request, mobile):
        # 获取图形验证码信息
        sro_image_code = request.GET.get('image_code')
        # 获取uuid
        uuid = request.GET.get('image_code_id')
        print(uuid)
        if not all([sro_image_code, uuid]):
            return JsonResponse({'code': 400, 'errmsg': '查询参数不完整'})
        # 链接存储短信验证码的redis
        msg_code_cli = get_redis_connection('msg_code')

        if msg_code_cli.get(mobile + '_flag'):
            return JsonResponse({'code': 400, 'errmsg': '获取短信验证码过于频繁，请稍后再获取'})

        image_code_cli = get_redis_connection('image_code')
        # 获取存储在redis中的uuid
        image_code = image_code_cli.get(uuid)

        print(image_code)

        if image_code is None:
            return JsonResponse({'code': 400, 'errmsg': '图形验证码已过期，请点击重新生成验证码'})
        # 验证图形验证码是否一致
        if image_code.decode().lower() != sro_image_code.lower():
            return JsonResponse({'code': 400, 'errmsg': '图形验证码不正确，请重新输入'})
        # 删除图形验证码，防止恶意刷图形验证码
        image_code_cli.delete(uuid)
        # 随机生成6位数短信验证码
        msg_code = '%06d' % randint(0, 999999)
        print(msg_code)

        # 设置管道
        msg_code_line = msg_code_cli.pipeline()
        # 保存短信验证码到redis中，同时保存一个标记到redis,防止恶意刷新短信验证码
        msg_code_line.setex(mobile, 300, msg_code)

        msg_code_line.setex(mobile + '_flag', 60, 1)
        # 提交到redis
        msg_code_line.execute()
        # CCP().send_template_sms('18768469597', [msg_code, 5], 1)
        # ccp_send_sms_code.delay(mobile, msg_code)

        return JsonResponse({'code': 200, 'errmsg': 'OK'})
