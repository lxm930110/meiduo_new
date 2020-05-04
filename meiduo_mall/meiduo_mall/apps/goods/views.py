from django.shortcuts import render
# Create your views here.
from django.core.paginator import Paginator, EmptyPage
from django.views import View
from goods.models import SKU, GoodsCategory, GoodsChannel
from django.http import JsonResponse
from meiduo_mall.utils.breadcrumb import get_breadcrumb
from haystack.views import SearchView


class ListView(View):

    def get(self, request, category_id):
        page_num = request.GET.get('page')
        page_size = request.GET.get('page_size')
        sort = request.GET.get('ordering')
        # 判断category_id是否正确
        try:
            # 获取三级菜单分类信息:
            cat3 = GoodsCategory.objects.get(pk=category_id)
        except:
            return JsonResponse({'code': 400,
                                 'errmsg': '获取mysql数据出错'})

        breadcrumb = get_breadcrumb(cat3)
        # # 获取二级菜单分类信息
        # cat2 = cat3.parent
        # # 获取一级菜单分类信息
        # cat1 = cat2.parent
        # breadcrumb = {
        #     'cat1': cat1.name,
        #     'cat2': cat2.name,
        #     'cat3': cat3.name,
        # }

        skus = SKU.objects.filter(category_id=category_id, is_launched=True).order_by(sort)
        # 创建分页对象，指定列表、页大小
        paginator = Paginator(skus, page_size)
        # 获取指定页码的数据
        page_skus = paginator.page(page_num)
        # 获取总页码数
        total_page = paginator.num_pages

        # 定义列表:
        list = []
        # 遍历:
        for sku in page_skus:
            list.append({
                'id': sku.id,
                'default_image_url': sku.default_image_url,
                'name': sku.name,
                'price': sku.price
            })
            # 把数据变为 json 发送给前端
        return JsonResponse({
            'code': 0,
            'errmsg': 'ok',
            'breadcrumb': breadcrumb,
            'list': list,
            'count': total_page
        })



class HotGoodsView(View):
    def get(self, request, category_id):
        try:
            skus = SKU.objects.filter(category_id=category_id,
                                      is_launched=True).order_by('-sales')[0:2]
        except Exception as e:
            return JsonResponse({'code': 400,
                                 'errmsg': '获取商品出错'})
        # 转换格式:
        hot_skus = []
        for sku in skus:
            hot_skus.append({
                'id': sku.id,
                'default_image_url': sku.default_image_url,
                'name': sku.name,
                'price': sku.price
            })

        return JsonResponse({'code': 0,
                             'errmsg': 'OK',
                             'hot_skus': hot_skus})



class MySearchView(SearchView):
    '''重写SearchView类'''
    def create_response(self):
        page = self.request.GET.get('page')
        # 获取搜索结果
        context = self.get_context()
        data_list = []
        for sku in context['page'].object_list:
            data_list.append({
                'id':sku.object.id,
                'name':sku.object.name,
                'price':sku.object.price,
                'default_image_url':sku.object.default_image_url,
                'searchkey':context.get('query'),
                'page_size':context['page'].paginator.num_pages,
                'count':context['page'].paginator.count
            })
        # 拼接参数, 返回
        return JsonResponse(data_list, safe=False)
