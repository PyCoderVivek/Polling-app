# Generated by Django 5.0.7 on 2024-09-19 09:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Poll', '0022_alter_poll_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='poll',
            name='image',
        ),
    ]
