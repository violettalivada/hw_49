# Generated by Django 2.2 on 2020-08-15 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0005_task_update_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='status',
            name='name',
            field=models.CharField(max_length=40, verbose_name='Статус'),
        ),
    ]
