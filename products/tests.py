from django.test import TestCase
from django.test.client import Client
from products.models import ProductCategory, Product
from django.core.management import call_command


class TestProductsSmoke(TestCase):
    def setUp(self):
        call_command('flush', '--noinput')
        call_command('loaddata', 'test_products.json')
        self.client = Client()

    def test_products_urls(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)
        for category in ProductCategory.objects.all():
            response = self.client.get(f'/products/{category.id}/')
            self.assertEqual(response.status_code, 200)

    def tearDown(self):
        call_command('sqlsequencereset', 'admins', 'baskets', 'ordersapp', 'products', 'users')

class TestProductsCase(TestCase):
    def setUp(self):
        category = ProductCategory.objects.create(name='shoes')
        self.product_first = Product.objects.create(name='sneakers',
                                                    category=category,
                                                    price=1000.1,
                                                    quantity=11)
        self.product_second = Product.objects.create(name='slippers',
                                                    category=category,
                                                    price=1300.3,
                                                    quantity=33)

    def test_product_get(self):
        product_first = Product.objects.get(name='sneakers')
        product_second = Product.objects.get(name='slippers')
        self.assertEqual(product_first, self.product_first)
        self.assertEqual(product_second, self.product_second)
