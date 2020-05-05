import os,django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meiduo_mall.settings.dev')
django.setup()
from goods.models import SKU
from django.conf import settings
from django.template import loader
from celery_tasks.main import celery_app
from meiduo_mall.utils import get_category,get_goods_desc


# 定义一个生成静态化页面的函数, 该函数需要用装饰器装饰:
@celery_app.task(name='generate_static_sku_detail_html')
def generate_static_sku_detail_html(sku_id):

    # 商品分类菜单
    dict = get_category.get_category()

    goods, specs, sku = get_goods_desc.get_goods_desc_info(sku_id)

    # 渲染模板，生成静态html文件
    context = {
        'categories': dict,
        'goods': goods,
        'specs': specs,
        'sku': sku
    }

    # 加载 loader 的 get_template 函数, 获取对应的 detail 模板
    template = loader.get_template('detail.html')
    # 拿到模板, 将上面添加好的数据渲染进去.
    html_text = template.render(context)
    # 拼接模板要生成文件的位置:
    file_path = os.path.join(settings.GENERATED_STATIC_HTML_FILES_DIR, 'goods/'+str(sku_id)+'.html')
    # 写入
    with open(file_path, 'w') as f:
        f.write(html_text)


if __name__ == '__main__':

    skus = SKU.objects.all()
    for sku in skus:
        generate_static_sku_detail_html(sku.id)