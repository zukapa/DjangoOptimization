from django.core.management.base import BaseCommand
from django.db.models import Q
from products.models import ProductCategory

class Command(BaseCommand):
    def handle(self, *args, **options):
        print(ProductCategory.objects.filter(Q(product__name='Синяя куртка The North Face') |
                                             Q(product__name='Черный рюкзак Nike Heritage')))
