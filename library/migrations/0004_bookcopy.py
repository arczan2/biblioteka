# Generated by Django 3.0 on 2020-12-10 22:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0003_book'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookCopy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(default=2020)),
                ('condition', models.CharField(default='brak informacji', max_length=100)),
                ('cover', models.CharField(choices=[('brak informacji', 'brak informacji'), ('miękka', 'miękka'), ('twarda', 'twarda')], default='brak informacji', max_length=20)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.Book')),
            ],
        ),
    ]