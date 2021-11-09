from django.urls import path
import admins.views as admins

app_name = 'admins'

urlpatterns = [
    path('', admins.index, name='index'),
    path('users/', admins.UserListView.as_view(), name='admin_users'),
    path('users-create/', admins.UserCreateView.as_view(), name='admin_users_create'),
    path('users-update/<int:pk>/', admins.UserUpdateView.as_view(), name='admin_users_update'),
    path('users-delete/<int:pk>/', admins.UserDeleteView.as_view(), name='admin_users_delete'),

    path('categories/create/', admins.category_create, name='category_create'),
    path('categories/read/', admins.categories, name='categories'),
    path('categories/update/<int:pk>/', admins.category_update, name='category_update'),
    path('categories/delete/<int:pk>/', admins.category_delete, name='category_delete'),

    path('products/create/category/<int:pk>/', admins.product_create, name='product_create'),
    path('products/read/category/<int:pk>/', admins.CategoryProductsReadView.as_view(), name='products'),
    path('products/read/<int:pk>/', admins.CategoryProductsReadView.as_view(), name='product_read'),
    path('products/update/<int:pk>/', admins.product_update, name='product_update'),
    path('products/delete/<int:pk>/', admins.product_delete, name='product_delete'),
]