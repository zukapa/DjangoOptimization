from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from datetime import timedelta
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail


class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', blank=True)
    age = models.PositiveIntegerField(verbose_name="age", default=18)
    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(default=(now() + timedelta(hours=48)))

    def is_activation_key_expired(self):
        if now() <= self.activation_key_expires:
            return False
        else:
            return True

    def save(self, *args, **kwargs):
        super(User, self).save()
        if not self.is_active:
            verify_link = reverse('users:commit', args=[self.email, self.activation_key])
            title = f'Подтверждение пользователя {self.username}'
            message = f'Для подтверждения пользователя {self.username} перейдите по ссылке: \n {settings.DOMAIN_NAME}{verify_link}'
            return send_mail(title, message, settings.EMAIL_HOST_USER, [self.email], fail_silently=True)