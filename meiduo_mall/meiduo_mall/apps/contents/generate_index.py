from collections import OrderedDict
import os, sys, django
import time


sys.path.insert(0, '../../../')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meiduo_mall.settings.dev')
# os.environ["DJANGO_SETTINGS_MODULE"] = "meiduo_mall.settings.dev"

django.setup()

from goods.models import GoodsChannel, GoodsCategory
from contents.models import ContentCategory, Content
from django.conf import settings
from django.template import loader

def generate_static_index_html():
    #　有序字典
    categories = OrderedDict()
    # 获取频道对象查询集
    channels = GoodsChannel.objects.order_by('group_id', 'sequence')
    # 遍历查询集
    for channel in channels:
        # 判断: 如果当前组id在不在有序字典中
        if channel.group_id not in categories:
            categories[channel.group_id] = {
                'channels':[],
                'sub_cats':[],
            }
        # 给一级分类添加数据
        categories[channel.group_id]['channels'].append({'id':channel.category.id,
                                                       'name':channel.category.name,
                                                       'url':channel.url})
        # 遍历出二级分类
        for sub2 in channel.category.goodscategory_set.all():
            # 给二级分类包含的三级分类添加数据
            sub2.sub_cats = sub2.goodscategory_set.all()
            # 给二级添加数据
            categories[channel.group_id]['sub_cats'].append(sub2)


        # 从 ContentCategory 广告模型类中获取所有数据
        content_category_list = ContentCategory.objects.filter()
        contents = {}
        # 遍历刚刚获取的所有数据
        for content_category in content_category_list:
            contents[content_category.key] = content_category.content_set.filter(status=True).order_by('sequence')

        context = {
            'categories': categories,
            'contents': contents
        }

        # 根据导入的 loader 获取 'index.html' 模板
        # template = loader.get_template('index.html')
        template = loader.get_template('index.html')

        # 拿到模板, 然后将 context 渲染到模板中, 生成渲染过的模板
        html_text = template.render(context)

        # 我们拼接新的 index.html 模板将要生成的所在地地址:
        file_path = os.path.join(settings.GENERATED_STATIC_HTML_FILES_DIR, 'index.html')

        # 以写的权限,将渲染过的模板重新生成, 写入到文件中.
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_text)


if __name__ == '__main__':

    generate_static_index_html()


