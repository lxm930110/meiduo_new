from django import http
from collections import OrderedDict
from goods.models import GoodsCategory
from goods.models import GoodsChannel, SKU
from goods.models import  SKUImage, SKUSpecification
from goods.models import  GoodsSpecification, SpecificationOption


def get_goods_desc_info(sku_id):
    # 获取单个商品对应的规格信息
    try:
        sku = SKU.objects.get(pk=sku_id)
        sku.images = sku.skuimage_set.all()
    except:
        return http.JsonResponse({'code':400,
                                  'errmsg':'获取数据失败'})
    specs = sku.skuspecification_set.order_by('spec_id')
    sku_spec = []
    for spec in specs:
        sku_spec.append(spec.option_id)

    # 获取所有商品对应的规格信息
    goods = sku.goods
    skus = goods.sku_set.all()
    dic = {}
    for sku1 in skus:
        spec_temps = sku1.skuspecification_set.order_by('spec_id')
        key = []
        for spec_temp in spec_temps:
            key.append(spec_temp.option_id)
        dic[tuple(key)]=sku1.id
    # 在每个选项上绑定对应的sku_id值
    specs = goods.goodsspecification_set.order_by('id')

    for index,good_spec in enumerate(specs):

        key = sku_spec[:]

        spec_options = good_spec.specificationoption_set.all()

        for spec_option in spec_options:
            key[index] = spec_option.id

            spec_option.sku_id = dic.get(tuple(key))

        good_spec.spec_options = spec_options

    return goods, specs, sku




