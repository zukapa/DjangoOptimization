from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from users.forms import UserLoginForm, UserRegisterForm, UserProfileForm, UserProfileFormTwo
from baskets.models import Basket
from baskets.models import User
from django.db import transaction


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = UserLoginForm()
    context = {'title': 'GeekShop - Авторизация', 'form': form}
    return render(request, 'users/login.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            save = form.save()
            if save[0] == 1:
                messages.success(request, 'Сообщение подтверждения пользователя отправлено')
                return HttpResponseRedirect(reverse('users:login'))
            else:
                messages.success(request, 'Ошибка отправки подтверждения пользователя')
                return HttpResponseRedirect(reverse('users:login'))
    else:
        form = UserRegisterForm()
    context = {'title': 'GeekShop - Регистрация', 'form': form}
    return render(request, 'users/register.html', context)


@transaction.atomic
@login_required
def profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(data=request.POST, files=request.FILES, instance=user)
        form_two = UserProfileFormTwo(data=request.POST, instance=user.userprofile)
        if form.is_valid() and form_two.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
    else:
        form = UserProfileForm(instance=user)
        form_two = UserProfileFormTwo(instance=user.userprofile)
    context = {'title': 'Geekshop - личный кабинет',
               'form': form,
               'form_two': form_two,
               'baskets': Basket.objects.filter(user=user).select_related()
               }
    return render(request, 'users/profile.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


def commit(request, email=None, activation_key=None):
    try:
        user = User.objects.get(email=email)
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            user.save()
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, f'Активация для пользователя {user} пройдена.')
            return render(request, 'users/commit.html')
        else:
            messages.success(request, f'Активация для пользователя {user} не пройдена.')
            return render(request, 'users/commit.html')
    except Exception as e:
        messages.success(request, f'Активация не пройдена: {e.args}')
        return render(request, 'users/commit.html')

