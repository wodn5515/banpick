# Generated by Django 3.0.4 on 2021-02-09 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('draft', '0012_remove_champion_keyword'),
    ]

    operations = [
        migrations.AddField(
            model_name='champion',
            name='keyword',
            field=models.CharField(default='', max_length=20, verbose_name='검색키워드'),
        ),
    ]