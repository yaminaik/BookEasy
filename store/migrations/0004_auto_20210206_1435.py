# Generated by Django 3.0.3 on 2021-02-06 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_review'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='create_at',
        ),
        migrations.RemoveField(
            model_name='review',
            name='update_at',
        ),
        migrations.AddField(
            model_name='review',
            name='rating',
            field=models.IntegerField(max_length=1, null=True),
        ),
    ]