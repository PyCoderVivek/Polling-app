# Generated by Django 5.0.7 on 2024-08-23 13:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Poll', '0007_polloption_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='polloption',
            name='photo',
        ),
    ]