from django.core.management.base import BaseCommand
from django.db.models import Q
from products.models import Product

class Command(BaseCommand):
    def handle(self, *args, **options):
        print(Product.objects.filter(Q(category__name='Аксессуары') | Q(category__name='Обувь')))
