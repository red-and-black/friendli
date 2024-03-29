# Generated by Django 3.2.13 on 2022-06-21 11:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('conversations', '0002_auto_20220530_0523'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='receiver',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='received_messages', to='auth.user'),
            preserve_default=False,
        ),
    ]
