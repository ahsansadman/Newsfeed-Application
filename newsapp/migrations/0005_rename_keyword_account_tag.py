# Generated by Django 3.2.9 on 2021-11-29 14:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('newsapp', '0004_auto_20211129_1202'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='keyword',
            new_name='tag',
        ),
    ]