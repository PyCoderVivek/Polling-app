# Generated by Django 5.0.7 on 2024-09-19 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Poll', '0021_alter_poll_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='poll_images/'),
        ),
    ]