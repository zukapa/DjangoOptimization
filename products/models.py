from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    desc = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='products_images', blank=True)
    desc = models.CharField(max_length=64, blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} | {self.category.name}'
