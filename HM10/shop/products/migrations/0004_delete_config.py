# Generated by Django 3.2.15 on 2023-01-04 11:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_config'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Config',
        ),
    ]