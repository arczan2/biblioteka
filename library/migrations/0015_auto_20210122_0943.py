# Generated by Django 3.0 on 2021-01-22 09:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('library', '0014_notification_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'verbose_name': 'Autora', 'verbose_name_plural': 'Autorzy'},
        ),
        migrations.AlterModelOptions(
            name='book',
            options={'verbose_name': 'Książka', 'verbose_name_plural': 'Książki'},
        ),
        migrations.AlterModelOptions(
            name='bookcopy',
            options={'verbose_name': 'Egzemplarz książki', 'verbose_name_plural': 'Egzemplarze książek'},
        ),
        migrations.AlterModelOptions(
            name='borrow',
            options={'verbose_name': 'Wypożyczenie', 'verbose_name_plural': 'Wypożyczenia'},
        ),
        migrations.AlterModelOptions(
            name='genre',
            options={'verbose_name': 'Gatunek', 'verbose_name_plural': 'Gatunki'},
        ),
        migrations.AlterModelOptions(
            name='notification',
            options={'verbose_name': 'Powiadomienie', 'verbose_name_plural': 'Powiadomienia'},
        ),
        migrations.RenameField(
            model_name='author',
            old_name='surrname',
            new_name='surname',
        ),
        migrations.RemoveField(
            model_name='borrow',
            name='borrow_extension',
        ),
        migrations.AlterField(
            model_name='author',
            name='name',
            field=models.CharField(max_length=40, verbose_name='Imię'),
        ),
        migrations.AlterField(
            model_name='author',
            name='nationality',
            field=models.TextField(default='narodowosc nieznana', max_length=50, verbose_name='Narodowość'),
        ),
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='library.Author', verbose_name='Autor'),
        ),
        migrations.AlterField(
            model_name='book',
            name='description',
            field=models.TextField(default='brak opisu', verbose_name='Opis'),
        ),
        migrations.AlterField(
            model_name='book',
            name='genre',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='library.Genre', verbose_name='Gatunek'),
        ),
        migrations.AlterField(
            model_name='book',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='book_images/', verbose_name='Ilustracja okładki'),
        ),
        migrations.AlterField(
            model_name='book',
            name='pages',
            field=models.IntegerField(verbose_name='Ilość stron'),
        ),
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(max_length=40, verbose_name='Tytuł'),
        ),
        migrations.AlterField(
            model_name='bookcopy',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.Book', verbose_name='Książka'),
        ),
        migrations.AlterField(
            model_name='bookcopy',
            name='condition',
            field=models.CharField(default='brak informacji', max_length=100, verbose_name='Stan książki'),
        ),
        migrations.AlterField(
            model_name='bookcopy',
            name='cover',
            field=models.CharField(choices=[('brak informacji', 'brak informacji'), ('miękka', 'miękka'), ('twarda', 'twarda')], default='brak informacji', max_length=20, verbose_name='Typ okładki'),
        ),
        migrations.AlterField(
            model_name='bookcopy',
            name='year',
            field=models.IntegerField(default=2020, verbose_name='Rok wydania'),
        ),
        migrations.AlterField(
            model_name='borrow',
            name='book_copy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.BookCopy', verbose_name='Egzemplarz książki'),
        ),
        migrations.AlterField(
            model_name='borrow',
            name='borrow_date',
            field=models.DateField(default=None, verbose_name='Data wypożyczenia'),
        ),
        migrations.AlterField(
            model_name='borrow',
            name='return_date',
            field=models.DateField(blank=True, default=None, null=True, verbose_name='Data oddania'),
        ),
        migrations.AlterField(
            model_name='borrow',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Użytkownik'),
        ),
        migrations.AlterField(
            model_name='genre',
            name='description',
            field=models.TextField(default='brak opisu', verbose_name='Opis'),
        ),
        migrations.AlterField(
            model_name='genre',
            name='name',
            field=models.CharField(max_length=20, unique=True, verbose_name='Gatunek'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='book_copy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.BookCopy', verbose_name='Egzemplarz książki'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='date',
            field=models.DateField(auto_now_add=True, verbose_name='Data'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='message',
            field=models.TextField(default='', verbose_name='Wiadomość'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='read',
            field=models.BooleanField(default=False, verbose_name='Czy odczytano?'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Użytkownik'),
        ),
        migrations.DeleteModel(
            name='BorrowExtension',
        ),
    ]
