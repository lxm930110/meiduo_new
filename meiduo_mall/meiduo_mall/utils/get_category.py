from collections import OrderedDict

from goods.models import GoodsChannel, GoodsCategory
from contents.models import ContentCategory, Content
from django.conf import settings
from django.template import loader


def get_category():

    categories = OrderedDict()
    # 获取频道对象查询集
    channels = GoodsChannel.objects.order_by('group_id', 'sequence')
    # 遍历查询集
    for channel in channels:
        # 判断: 如果当前组id在不在有序字典中
        if channel.group_id not in categories:
            categories[channel.group_id] = {
                'channels': [],
                'sub_cats': [],
            }
        # 给一级分类添加数据
        categories[channel.group_id]['channels'].append({'id': channel.category.id,
                                                         'name': channel.category.name,
                                                         'url': channel.url})
        # 遍历出二级分类
        for sub2 in channel.category.goodscategory_set.all():
            # 给二级分类包含的三级分类添加数据
            sub2.sub_cats = sub2.goodscategory_set.all()
            # 给二级添加数据
            categories[channel.group_id]['sub_cats'].append(sub2)

    return categories

