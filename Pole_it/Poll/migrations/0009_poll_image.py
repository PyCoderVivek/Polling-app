# Generated by Django 5.0.7 on 2024-08-23 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Poll', '0008_remove_polloption_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='poll',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='poll_images/'),
        ),
    ]