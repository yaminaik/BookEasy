# Generated by Django 3.1.6 on 2021-02-14 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_comment_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
