from django.urls import path
import orders.views as orders

app_name = 'orders'

urlpatterns = [
    path('', orders.OrderList.as_view(), name='orders_list'),
    path('forming/complete/<int:pk>/', orders.order_forming_complete, name='order_forming_complete'),
    path('create/', orders.OrderCreate.as_view(), name='order_create'),
    path('read/<int:pk>/', orders.OrderRead.as_view(), name='order_read'),
    path('update/<int:pk>/', orders.OrderUpdate.as_view(), name='order_update'),
    path('delete/<int:pk>/', orders.OrderDelete.as_view(), name='order_delete'),
    path('product/<int:pk>/price/', orders.get_product_price)
]