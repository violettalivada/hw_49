# Generated by Django 2.2 on 2020-08-15 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0004_auto_20200812_1647'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='update_date',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата изменения'),
        ),
    ]
