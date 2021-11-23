from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string
from django.http import JsonResponse

from datetime import datetime
from products.models import ProductCategory, Product
from baskets.models import Basket


def index(request):
    context = {'title': 'GeekShop111',
               'date': datetime.now()}
    return render(request, 'products/index.html', context)


def products(request, category_id=None, page=1):
    if category_id:
        # category = ProductCategory.objects.get(id=category_id)
        # products = Product.objects.filter(category=category)
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()
    context = {'title': 'GeekShop-Catalog',
               'categories': ProductCategory.objects.all()}
    paginator = Paginator(products, 3)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)
    context['products'] = products_paginator
    return render(request, 'products/products.html', context)


@login_required
def item_add(request, id):
    if request.is_ajax():
        item = Product.objects.get(id=id)
        baskets = Basket.objects.filter(user=request.user, product=item)
        if not baskets.exists():
            Basket.objects.create(user=request.user, product=item, quantity=1)
        else:
            basket = baskets.first()
            if item.quantity - basket.quantity > 0:
                basket.quantity += 1
                basket.save()
            else:
                messages.error(request, item.name + ' - закончились.')
        # baskets = Basket.objects.filter(user=request.user)
        # print(baskets, baskets.total_quantity())
        # context = {'baskets': Basket.total_quantity(baskets)}
        # result = render_to_string('products/base.html', context)
        # print(result)
        # return JsonResponse({'result': result})
        return HttpResponse(request)

    # product = Product.objects.get(id=product_id)
    # baskets = Basket.objects.filter(user=request.user, product=product)
    # if not baskets.exists():
    #     Basket.objects.create(user=request.user, product=product, quantity=1)
    #     return HttpResponseRedirect(request.META['HTTP_REFERER'])
    # else:
    #     basket = baskets.first()
    #     if product.quantity - basket.quantity > 0:
    #         basket.quantity += 1
    #         basket.save()
    #     else:
    #         messages.error(request, product.name + ' - закончились.')
    #     return HttpResponseRedirect(request.META['HTTP_REFERER'])