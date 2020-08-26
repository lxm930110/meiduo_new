from django.urls import re_path
from rest_framework_jwt.views import obtain_jwt_token

from meiduo_admin.views.Channel import GoodsChannelModelViewSet
from meiduo_admin.views.admin import UserModelViewSet
from meiduo_admin.views.brand import BrandModelViewSet
from meiduo_admin.views.image import ImageModelViewSet, SimpleListAPIView
# from meiduo_admin.views.orders import OrderListAPIView, OrderDetailListAPIView, OrderUpdateAPIView
from meiduo_admin.views.orders import OrderReadOnlyModelViewSet
from meiduo_admin.views.permission import PermissionModelViewSet
from meiduo_admin.views.permissiongroup import GroupModelViewSet

from meiduo_admin.views.sku import GoodsCategory3ListAPIView, GoodsListAPIView, SkuSetView, SpuListAPIView

from meiduo_admin.views.spu import SPUModelViewSet, GoodsBrandListAPIView, GoodsCategory1ListAPIView, \
    Goods2Category3ListAPIView
from .views import statistical
from .views import user
from rest_framework.routers import SimpleRouter,DefaultRouter

from meiduo_admin.views.SpecificationOption import SpecOptionListAPIView

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
    # # 获取SKU
    # re_path(r'^skus/$', SkuListAPIView.as_view()),
    # 获取三级分类商品
    re_path(r'^skus/categories/$', GoodsCategory3ListAPIView.as_view()),
    # 获取SPU商品
    re_path(r'^goods/simple/$', GoodsListAPIView.as_view()),
    # 获取SPU规格
    re_path(r'^goods/(?P<pk>\d+)/specs/$', SpuListAPIView.as_view()),

    # 获取Brand列表
    re_path(r'^goods/brands/simple/$', GoodsBrandListAPIView.as_view()),

    # 获取category1列表
    re_path(r'^goods/channel/categories/$', GoodsCategory1ListAPIView.as_view()),
    # 获取category列表
    re_path(r'^goods/channel/categories/(?P<pk>\d+)/$', Goods2Category3ListAPIView.as_view()),

    #
    # 获取goods/specs/simple列表
    re_path(r'^goods/specs/simple/$', SpecOptionListAPIView.as_view()),


    # 获取content_types列表
    re_path(r'^permission/content_types/$', PermissionModelViewSet.as_view({'get':'content_types'})),

    # 获取permission/simple列表
    re_path(r'^permission/simple/$', GroupModelViewSet.as_view({'get': 'simple'})),

    # 获取permission/simple列表
    re_path(r'^permission/groups/simple/$', UserModelViewSet.as_view({'get': 'groups_simple'})),


]





router = DefaultRouter()

# 获取图片列表
router.register('skus/images', ImageModelViewSet, basename='images')


# permission

router.register('permission/perms', PermissionModelViewSet, basename='perms')


# 获取用户组表列表数据

router.register('permission/groups', GroupModelViewSet, basename='groups')


# 获取admin表列表数据

router.register('permission/admins', UserModelViewSet, basename='admins')



# Specification

from meiduo_admin.views.specifaction import SpecificationModelViewSet

router.register('goods/specs', SpecificationModelViewSet, basename='specs')

# SpecificationOption

from meiduo_admin.views.SpecificationOption import SpecificationOptionModelViewSet, SpecOptionListAPIView

router.register('specs/options', SpecificationOptionModelViewSet, basename='options')

# SKU

router.register('skus', SkuSetView, basename='skus')


# 获取订单

router.register('orders', OrderReadOnlyModelViewSet, basename='orders')


# brand

router.register('goods/brands', BrandModelViewSet, basename='brands')


# channel

router.register('goods/channels', GoodsChannelModelViewSet, basename='channels')



# SPU

router.register('goods', SPUModelViewSet, basename='goods')



urlpatterns += router.urls

print(router.urls)
