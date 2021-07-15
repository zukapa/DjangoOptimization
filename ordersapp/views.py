from django.shortcuts import get_object_or_404, HttpResponseRedirect
from django.db import transaction
from django.forms import inlineformset_factory
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from baskets.models import Basket
from ordersapp.models import Order, OrderItem
from ordersapp.forms import OrderItemForm
from django.urls import reverse_lazy, reverse
from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete


class OrderList(ListView):
    model = Order

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderCreate(CreateView):
    model = Order
    fields = []
    success_url = reverse_lazy('ordersapp:order_list')

    def get_context_data(self, **kwargs):
        data = super(OrderCreate, self).get_context_data(**kwargs)
        order_formset = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)
        if self.request.POST:
            formset = order_formset(self.request.POST)
        else:
            baskets = Basket.objects.filter(user=self.request.user)
            if len(baskets):
                order_formset = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=len(baskets))
                formset = order_formset()
                for num, form in enumerate(formset.forms):
                    form.initial['product'] = baskets[num].product
                    form.initial['quantity'] = baskets[num].quantity
                    form.initial['price'] = baskets[num].product.price
                baskets.delete()
            else:
                formset = order_formset()
        data['order_items'] = formset
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        order_items = context['order_items']
        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if order_items.is_valid():
                order_items.instance = self.object
                order_items.save()
        if self.object.get_total_cost() == 0:
            self.object.delete()
        return super(OrderCreate, self).form_valid(form)


class OrderUpdate(UpdateView):
    model = Order
    fields = []
    success_url = reverse_lazy('ordersapp:order_list')

    def get_context_data(self, **kwargs):
        data = super(OrderUpdate, self).get_context_data(**kwargs)
        order_formset = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)
        if self.request.POST:
            data['order_items'] = order_formset(self.request.POST, instance=self.object)
        else:
            formset = order_formset(instance=self.object)
            for form in formset.forms:
                if form.instance.pk:
                    form.initial['price'] = form.instance.product.price
            data['order_items'] = formset
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        order_items = context['order_items']
        with transaction.atomic():
            self.object = form.save()
            if order_items.is_valid():
                order_items.instance = self.object
                order_items.save()
        if self.object.get_total_cost() == 0:
            self.object.delete()
        return super(OrderUpdate, self).form_valid(form)


class OrderDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('ordersapp:order_list')


class OrderRead(DetailView):
    model = Order

    def get_context_data(self, **kwargs):
        context = super(OrderRead, self).get_context_data(**kwargs)
        context['title'] = 'Заказ/просмотр'
        return context


def change_status(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SENT_TO_PROCEED
    order.save()
    return HttpResponseRedirect(reverse('ordersapp:order_list'))


@receiver(pre_save, sender=OrderItem)
@receiver(pre_save, sender=Basket)
def product_quantity_update_save(sender, update_fields, instance, **kwargs):
    if update_fields is 'quantity' or 'product':
        if instance.pk:
            instance.product.quantity -= instance.quantity - \
                                         sender.get_item(instance.pk).quantity
        else:
            instance.product.quantity -= instance.quantity
        instance.product.save()


@receiver(pre_delete, sender=OrderItem)
@receiver(pre_delete, sender=Basket)
def product_quantity_update_delete(sender, instance, **kwargs):
    instance.product.quantity += instance.quantity
    instance.product.save()
