from django.shortcuts import render, reverse, HttpResponseRedirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from users.models import User
from products.models import Product, ProductCategory
from admins.forms import UserAdminRegistrationForm, UserAdminProfileForm, ProductEditForm


@user_passes_test(lambda u: u.is_staff)
def index(request):
    context = {'title': 'GeekShop - Админ панель'}
    return render(request, 'admins/index.html', context)


class UserListView(ListView):
    model = User
    template_name = 'admins/admin-users-read.html'

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(UserListView, self).dispatch(request, *args, **kwargs)


class UserCreateView(CreateView):
    model = User
    form_class = UserAdminRegistrationForm
    success_url = reverse_lazy('admins:admin_users')
    template_name = 'admins/admin-users-create.html'


class UserUpdateView(UpdateView):
    model = User
    form_class = UserAdminProfileForm
    success_url = reverse_lazy('admins:admin_users')
    template_name = 'admins/admin-users-update-delete.html'

    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop - Обновление пользователя'
        return context


class UserDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy('admins:admin_users')
    template_name = 'admins/admin-users-update-delete.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.safe_delete()
        return HttpResponseRedirect(success_url)

# @user_passes_test(lambda u: u.is_staff)
# def admin_users(request):
#     context = {
#         'title': 'GeekShop - Пользователи',
#         'users': User.objects.all(),
#     }
#     return render(request, 'admins/admin-users-read.html', context)

# CRUD
# @user_passes_test(lambda u: u.is_staff)
# def admin_users_create(request):
#     if request.method == 'POST':
#         form = UserAdminRegistrationForm(data=request.POST, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('admins:admin_users'))
#     else:
#         form = UserAdminRegistrationForm()
#     context = {'title': 'GeekShop - Создание пользователя', 'form': form}
#     return render(request, 'admins/admin-users-create.html', context)

#
# @user_passes_test(lambda u: u.is_staff)
# def admin_users_update(request, id):
#     selected_user = User.objects.get(id=id)
#     if request.method == 'POST':
#         form = UserAdminProfileForm(instance=selected_user, files=request.FILES, data=request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('admins:admin_users'))
#     else:
#         form = UserAdminProfileForm(instance=selected_user)
#     context = {
#         'title': 'GeekShop - Обновление пользователя',
#         'form': form,
#         'selected_user': selected_user
#     }
#     return render(request, 'admins/admin-users-update-delete.html', context)

#
# @user_passes_test(lambda u: u.is_staff)
# def admin_users_delete(request, id):
#     user = User.objects.get(id=id)
#     # user.delete()
#     user.safe_delete()
#     return HttpResponseRedirect(reverse('admins:admin_users'))

def categories(request):
    title = 'админка/категории'

    categories_list = ProductCategory.objects.all()

    content = {
        'title': title,
        'objects': categories_list
    }

    return render(request, 'admins/categories.html', content)


def category_create(request):
    pass


def category_update(request, pk):
    pass


def category_delete(request, pk):
    pass


def products(request, pk):
    title = 'админка/продукт'

    category = get_object_or_404(ProductCategory, pk=pk)
    products_list = Product.objects.filter(category__pk=pk).order_by('name')

    content = {
        'title': title,
        'category': category,
        'objects': products_list,
    }

    return render(request, 'admins/products.html', content)


def product_create(request, pk):
    title = 'товары/создание'
    category = get_object_or_404(ProductCategory, pk=pk)

    if request.method == 'POST':
        product_form = ProductEditForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()
            return HttpResponseRedirect(reverse('admins:products', args=[pk]))
    else:
        product_form = ProductEditForm(initial={'category': category})

    context = {
        'title': title,
        'product_form': product_form,
        'category': category,
    }

    return render(request, 'admins/product_update.html', context)


class CategoryProductsReadView(ListView):
    model = Product
    context_object_name = 'objects'
    template_name = 'admins/products.html'

    def get_queryset(self):
        filtered_products = Product.objects.filter(category__pk=self.kwargs['pk'])
        return filtered_products

    def get_context_data(self):
        context = super(CategoryProductsReadView, self).get_context_data()
        context['category'] = self.kwargs.get('pk')
        return context

# def product_read(request, pk):
#     title = 'продукт/подробнее'
#     product = get_object_or_404(Product, pk=pk)
#     context = {'title': title, 'object': product, }
#
#     return render(request, 'admins/product_read.html', context)


def product_update(request, pk):
    title = 'товары/редактирование'

    edit_product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        edit_form = ProductEditForm(request.POST, request.FILES, instance=edit_product)

        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admins:product_update', args=[edit_product.pk]))
    else:
        edit_form = ProductEditForm(instance=edit_product)

    context = {
        'title': title,
        'product_form': edit_form
    }

    return render(request, 'admins/product_update.html', context)


def product_delete(request, pk):
    title = 'продукт/удаление'

    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.is_active = False
        product.save()
        return HttpResponseRedirect(reverse('admins:products', args=[product.category.pk]))

    context = {'title': title, 'product_to_delete': product}

    return render(request, 'admins/product_delete.html', context)