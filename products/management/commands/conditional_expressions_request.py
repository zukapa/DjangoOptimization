from django.db.models import F, Q, When, Case, DecimalField, IntegerField
from datetime import timedelta
from ordersapp.models import OrderItem
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        action_1 = 1
        action_expired = 3
        action_1_time_delta = timedelta(hours=12)
        action_2_time_delta = timedelta(days=1)
        action_1_discount = 0.5
        action_expired_discount = 0.1
        action_1_condition = Q(order__updated__lte=F('order__created') + action_1_time_delta)
        action_expired_condition = Q(order__updated__gt=F('order__created') + action_2_time_delta)
        action_1_order = When(action_1_condition, then=action_1)
        action_expired_order = When(action_expired_condition, then=action_expired)
        action_1_price = When(action_1_condition, then=F('product__price') * F('quantity') * action_1_discount)
        action_expired_price = When(action_expired_condition, then=F('product__price') * F('quantity') * action_expired_discount)
        orders = OrderItem.objects.annotate(
            action_order=Case(
                action_1_order,
                action_expired_order,
                output_field=IntegerField(),
            )).annotate(
            total_price=Case(
                action_1_price,
                action_expired_price,
                output_field=DecimalField(),
            )).order_by('action_order', 'total_price').select_related()
        for item in orders:
            print(f'{item.action_order}: заказ №{item.pk}:'
                f'{item.product.name:15}: скидка '
                f'{abs(item.total_price):6.2f} руб. | '
                f'{item.order.updated - item.order.created}')
