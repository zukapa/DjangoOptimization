from django.urls import path

from admins.views import index, UserListView, UserUpdateView, UserCreateView, UserDeleteView, ProductCategoryUpdateView
from admins.views import ProductCategoryListView

app_name = 'admins'

urlpatterns = [
    path('', index, name='index'),
    path('users/', UserListView.as_view(), name='admin_users'),
    path('users/create/', UserCreateView.as_view(), name='admin_users_create'),
    path('users/update/<int:pk>', UserUpdateView.as_view(), name='admin_users_update'),
    path('users/delete/<int:pk>', UserDeleteView.as_view(), name='admin_users_delete'),
    path('categories/', ProductCategoryListView.as_view(), name='categories'),
    path('categories/update/<int:pk>', ProductCategoryUpdateView.as_view(), name='categories_update')
]
