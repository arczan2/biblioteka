# Generated by Django 3.0 on 2021-01-15 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0010_auto_20210115_1328'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='description',
            field=models.TextField(default='brak opisu'),
        ),
    ]
