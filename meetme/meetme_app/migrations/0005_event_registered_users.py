# Generated by Django 4.1.3 on 2022-11-12 20:28

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('meetme_app', '0004_alter_meetingrequest_options_meetingrequest_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='registered_users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
