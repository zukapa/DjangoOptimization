from baskets.models import Basket
from django.contrib.auth.decorators import login_required


@login_required
def baskets_context(request):
    basket_len = len(Basket.objects.filter(user=request.user))
    return {'basket_len': basket_len}
