# Generated by Django 3.1.6 on 2021-03-22 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0014_remove_comment_subject'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='subject',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
