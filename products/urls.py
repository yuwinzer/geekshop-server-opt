from django.urls import path
from products.views import products, item_add

app_name = 'products'

urlpatterns = [
    path('', products, name='index'),  # .../products/
    path('<int:category_id>', products, name='category'),  # /products/<category_id>/
    path('page/<int:page>', products, name='page'),  # /products/<category_id>/
    path('add/<int:id>/', item_add, name='item_add'),
]