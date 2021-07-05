from django.urls import path

from users.views import login, register, logout, profile, commit

app_name = 'users'

urlpatterns = [
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('logout/', logout, name='logout'),
    path('commit/<str:email>/<str:activation_key>/', commit, name='commit')
]
