from django.urls import re_path
from rest_framework_jwt.views import obtain_jwt_token

from meiduo_admin.views.image import ImageModelViewSet, SimpleListAPIView
# from meiduo_admin.views.orders import OrderListAPIView, OrderDetailListAPIView, OrderUpdateAPIView
from meiduo_admin.views.orders import OrderReadOnlyModelViewSet

from meiduo_admin.views.sku import SkuSetView
from .views import statistical
from .views import user
from rest_framework.routers import SimpleRouter,DefaultRouter

urlpatterns = [
    #　登录
    re_path(r'^authorizations/$', obtain_jwt_token),
    # 统计用户总数
    re_path(r'^statistical/total_count/$', statistical.StatisticalCountUser.as_view()),
    # 统计日增用户
    re_path(r'^statistical/day_increment/$', statistical.StatisticalCountincrementUser.as_view()),
    # 统计日活跃用户
    re_path(r'^statistical/day_active/$', statistical.StatisticalCountActiveUser.as_view()),
    # 统计日下单用户
    re_path(r'^statistical/day_orders/$', statistical.StatisticalCountOrdersUser.as_view()),
    # 统计月增用户
    re_path(r'^statistical/month_increment/$', statistical.StatisticalMonthCountUser.as_view()),
    # 日分类商品访问量
    re_path(r'^statistical/goods_day_views/$', statistical.StatisticalCountDetailVisitUser.as_view()),

    #############################################User###################################
    # 统计月增用户
    re_path(r'^users/$', user.UserView.as_view()),

    # 更新商品图片
    re_path(r'^skus/simple/$', SimpleListAPIView.as_view()),

    ########################################
    # order列表
    # re_path(r'^orders/$', OrderListAPIView.as_view()),
    # # order详情页
    # re_path(r'^orders/(?P<pk>\d+)/$', OrderDetailListAPIView.as_view()),
    # # order修改
    # re_path(r'^orders/(?P<order_id>\d+)/status/$', OrderUpdateAPIView.as_view()),
]

# 获取图片列表

router = DefaultRouter()

router.register('skus/images', ImageModelViewSet, basename='images')

urlpatterns += router.urls


# 商品管理
router = DefaultRouter()

router.register('skus', SkuSetView, basename='skus')

urlpatterns += router.urls




# 获取订单

router = DefaultRouter()

router.register('orders', OrderReadOnlyModelViewSet, basename='orders')

urlpatterns += router.urls
