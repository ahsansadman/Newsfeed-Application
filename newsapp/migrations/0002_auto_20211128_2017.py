# Generated by Django 3.2.9 on 2021-11-28 20:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('newsapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='source',
            options={'ordering': ['id']},
        ),
        migrations.RemoveField(
            model_name='account',
            name='source',
        ),
        migrations.AddField(
            model_name='source',
            name='account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='newsapp.account'),
        ),
    ]
