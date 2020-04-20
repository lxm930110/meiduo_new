from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from django_redis import get_redis_connection

from meiduo_mall.libs.captcha.captcha import captcha


# Create your views here.

class ImageCode(View):
    def get(self, request, uuid):
        # 通过调用generate_captcha()方法获取图像验证码
        name, text, image = captcha.generate_captcha()
        redis_cli = get_redis_connection('verfiy_code')
        redis_cli.setex(uuid, 60 * 5, uuid)
        return HttpResponse(image, content_type='image/jpg')
