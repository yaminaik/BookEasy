# Generated by Django 3.1.6 on 2021-03-01 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_auto_20210301_0938'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='orderinfo',
        ),
        migrations.AlterField(
            model_name='orderinfo',
            name='order_id',
            field=models.IntegerField(),
        ),
    ]
