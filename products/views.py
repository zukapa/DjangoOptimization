from django.shortcuts import render
from django.conf import settings
from django.core.cache import cache
from products.models import ProductCategory, Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):
    context = {
        'title': 'GeekShop',
    }
    return render(request, 'products/index.html', context)


def products(request, category_id=None, page=1):
    if settings.LOW_CACHE:      # After applying memcached, the page loads in 34 milliseconds, before - 60 milliseconds
        key = 'products_products'
        products_products = cache.get(key)
        if products_products is None:
            products_products = ProductCategory.objects.all().select_related()
            cache.set(key, products_products)
    else:
        products_products = ProductCategory.objects.all().select_related()
    context = {'title': 'GeekShop-Каталог', 'category': products_products}
    product = Product.objects.filter(category_id=category_id).select_related('category')[:3] if category_id else \
        Product.objects.all().select_related()
    paginator = Paginator(product, 3)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)
    context['products'] = products_paginator
    return render(request, 'products/products.html', context)
