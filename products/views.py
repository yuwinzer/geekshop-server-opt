from django.shortcuts import render
from products.models import Product, ProductCategory
import os
import json
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

MODULE_DIR = os.path.dirname(__file__)

# Create your views here.
def index(request):
    context = {'title': 'Geekshop',
               'date': datetime.now()}
    return render(request, 'products/index.html', context)


def products(request, category_id=None, page=1):
    # file_path_prod = os.path.join(MODULE_DIR, 'fixtures/goods.json') # подгрузка данных из fixtures
    # file_path_cat = os.path.join(MODULE_DIR, 'fixtures/categories.json') # подгрузка данных из fixtures
    context = {'title': 'Geekshop - catalog',
               'categories': ProductCategory.objects.all()
               # 'products': json.load(open(file_path_prod, encoding='utf-8')),  # подгрузка данных из fixtures
               # 'categories': json.load(open(file_path_cat, encoding='utf-8'))  # подгрузка данных из fixtures
               }
    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()
    paginator = Paginator(products, 3)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)
    context['products'] = products_paginator
    return render(request, 'products/products.html', context)