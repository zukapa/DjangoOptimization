from django.db import models
from django.utils.functional import cached_property
from users.models import User
from products.models import Product


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Корзина для {self.user.username} | Продукт{self.product.name}'

    @cached_property
    def get_items_cached(self):
        return Basket.objects.filter(user=self.user)

    def sum(self):
        return self.quantity * self.product.price

    def total_quantity(self):
        baskets = self.get_items_cached
        return sum(basket.quantity for basket in baskets)

    @staticmethod
    def get_item(pk):
        return Basket.objects.get(id=pk)

    def total_sum(self):
        baskets = self.get_items_cached
        return sum(basket.sum() for basket in baskets)