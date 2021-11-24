from django.contrib import admin

from orders.models import Order, OrderItem


# admin.site.register(OrderList)


class OrderItemsAdmin(admin.TabularInline):
    model = OrderItem
    fields = ('product', 'quantity',)
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'id', 'user', 'status',
                    'get_total_quantity', 'get_total_cost',
                    'created', 'updated', 'is_active',)
    fields = ('id',
              'user',
              ('get_total_quantity', 'get_total_cost'),
              'status',
              'is_active',
              'created',
              'updated',)
    readonly_fields = ('id', 'user', 'created', 'updated', 'get_total_quantity', 'get_total_cost')
    inlines = (OrderItemsAdmin,)
    ordering = ('id', 'user')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'user__id',)

