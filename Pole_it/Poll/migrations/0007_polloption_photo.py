# Generated by Django 5.0.7 on 2024-08-23 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Poll', '0006_delete_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='polloption',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='poll_option_photos/'),
        ),
    ]