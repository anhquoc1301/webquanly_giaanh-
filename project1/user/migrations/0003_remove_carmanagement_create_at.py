# Generated by Django 3.2.5 on 2021-07-17 10:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_carmanagement'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carmanagement',
            name='create_at',
        ),
    ]
