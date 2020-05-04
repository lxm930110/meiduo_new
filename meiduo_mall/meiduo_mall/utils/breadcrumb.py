
def get_breadcrumb(cat3):
    # 获取二级菜单分类信息
    cat2 = cat3.parent
    # 获取一级菜单分类信息
    cat1 = cat2.parent
    breadcrumb = {
        'cat1': cat1.name,
        'cat2': cat2.name,
        'cat3': cat3.name,
    }
    return breadcrumb