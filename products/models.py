from django.db import models

# модели = таблицы в бд

class ProductCategory(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=256)
    image = models.ImageField(upload_to='products_images')
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=8,decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} | {self.category.name}'

    # for orders formset:
    @staticmethod
    def get_items():
        return Product.objects.filter(quantity__gte=1).order_by('category', 'name')


