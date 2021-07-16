from ordersapp.views import OrderList, change_status, OrderCreate, OrderRead, OrderUpdate, OrderDelete
from django.urls import path

app_name = 'ordersapp'

urlpatterns = [
   path('', OrderList.as_view(), name='order_list'),
   path('status_change/<int:pk>/', change_status, name='status_change'),
   path('create/', OrderCreate.as_view(), name='create'),
   path('read/<int:pk>/', OrderRead.as_view(), name='read'),
   path('update/<int:pk>/', OrderUpdate.as_view(), name='update'),
   path('delete/<int:pk>/', OrderDelete.as_view(), name='delete'),
]