# Generated by Django 5.0.7 on 2024-09-04 08:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Poll', '0012_poll_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='poll',
            name='likes',
        ),
    ]