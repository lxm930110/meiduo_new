# from celery_tasks.main import app
# from meiduo_mall.libs.yuntongxun.sms import CCP
# from . import constants

from celery_tasks.main import celery_app
from meiduo_mall.libs.yuntongxun.sms import CCP


@celery_app.task(name='ccp_send_sms_code')
def ccp_send_sms_code(mobile, msg_code):
    '''该函数就是一个任务, 用于发送短信'''
    result = CCP().send_template_sms(mobile,
                                     [msg_code, 5],
                                     1)
    return result


# @app.task(bind=True, name='send_sms', retry_backoff=3)
# def send_sms(self, mobile, sms_code):
#     # 将耗时的代码封装在一个方法中
#     ccp = CCP()
#     ret= ccp.send_template_sms(mobile, [sms_code, constants.SMS_CODE_EXPIRES], 1)
#     if ret !=0:
#         raise self.retry(exc=Exception('发送短信失败'), max_retries=3)
#     return ret
#
#     # print(sms_code)
#
# def hello():
#     print('ok')