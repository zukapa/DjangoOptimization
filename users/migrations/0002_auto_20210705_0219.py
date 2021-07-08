# Generated by Django 3.2.3 on 2021-07-04 23:19

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='activation_key',
            field=models.CharField(blank=True, max_length=128),
        ),
        migrations.AddField(
            model_name='user',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 6, 23, 19, 30, 326545, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='user',
            name='age',
            field=models.PositiveIntegerField(default=18, verbose_name='age'),
        ),
    ]
