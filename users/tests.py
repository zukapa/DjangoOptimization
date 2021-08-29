from django.test import TestCase
from django.test.client import Client
from users.models import User
from django.core.management import call_command


class TestUsersAuth(TestCase):
    def setUp(self):
        call_command('flush', '--noinput')
        call_command('loaddata', 'test_products.json')
        self.client = Client()
        self.superuser = User.objects.create_superuser('django_test_su', '123@mail.ru', 'Ghbdtn12')
        self.user = User.objects.create_user('django_test', '321@mail.ru', 'Ghbdtn12')

    def test_login(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)
        self.assertEqual(response.context['title'], 'GeekShop')
        self.assertNotContains(response, 'Выйти ', status_code=200)
        self.client.login(username='django_test', password='Ghbdtn12')
        response = self.client.get('/')
        self.assertFalse(response.context['user'].is_anonymous)
        self.assertEqual(response.context['user'], self.user)
        self.assertContains(response, 'Выйти ', status_code=200)

    def test_basket_redirect(self):
        response = self.client.get('/users/profile/')
        self.assertEqual(response.url, '/users/login/?next=/users/profile/')
        self.assertEqual(response.status_code, 302)
        self.client.login(username='django_test', password='Ghbdtn12')
        response = self.client.get('/users/profile/')
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        call_command('sqlsequencereset', 'admins', 'baskets', 'ordersapp', 'products', 'users')
