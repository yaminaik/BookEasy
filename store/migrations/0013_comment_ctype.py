# Generated by Django 3.1.6 on 2021-03-01 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_auto_20210301_0957'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='ctype',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
