# Generated by Django 5.0.7 on 2024-09-17 07:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Poll', '0015_vote_timestamp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vote',
            name='timestamp',
        ),
    ]
