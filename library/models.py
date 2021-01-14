from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from enum import Enum
import datetime


class Genre(models.Model):
    name = models.CharField(max_length=20, unique=True, null=False, blank=False)
    description = models.TextField(default='brak opisu')

    def clean(self):
        from django.core.exceptions import ValidationError
        # Jeżeli nazwa książki jest pusta to zwróć wyjątek
        if self.name is None or self.name == '':
            raise ValidationError('Nazwa gatunku nie moze być pusta')
        # Sprawdz czy gatunek o tej nazwie juz istnieje w bazie
        if self.name.lower() in [names['name'].lower() for names in
                                 Genre.objects.all().values('name')]:
            raise ValidationError('Gatunek o tej nazwie już istnieje')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Walidacja danych przed próbą zapisania
        self.clean()
        super().save(*args, **kwargs)


class Author(models.Model):
    name = models.CharField(max_length=40, null=False)
    surrname = models.CharField(max_length=40, null=False,)
    nationality = models.TextField(max_length=50, default='narodowosc nieznana')

    def clean(self):
        from django.core.exceptions import ValidationError

        if self.name is None or self.name == '' or self.surrname is None or self.surrname == '':
            raise ValidationError('Imię i nazwisko to pola wymagane i nie mogą byc puste')

        if self.name.lower() in [names['name'].lower() for names in
            Author.objects.all().values('name')] and self.surrname.lower() in [surrnames['surrname'].lower() for surrnames in
            Author.objects.all().values('surrname')] and self.nationality.lower() in [nationalities['nationality'].lower() for nationalities in
            Author.objects.all().values('nationality')]:
                raise ValidationError('Taka osoba już istnieje w bazie autorów')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name + " " + self.surrname


class Book(models.Model):
    title = models.CharField(max_length=40)
    pages = models.IntegerField()
    genre = models.ForeignKey(Genre, null=True, on_delete=models.SET_NULL,
                              blank=True)
    author = models.ForeignKey(Author, null=True, on_delete=models.SET_NULL,
                               blank=True)

    def clean(self):
        from django.core.exceptions import ValidationError
        # Jeżeli tytul książki jest pusta to zwróć wyjątek
        if self.title is None or self.title == '':
            raise ValidationError('Tytul ksiazki nie moze być pusta')
        # Sprawdz czy ksiazka o tem tytule juz istnieje w bazie
        if self.title.lower() in [titles['title'].lower() for titles in
                                 Book.objects.all().values('title')]:
            raise ValidationError('Ksiazka o tym tytule juz istnieje')

    def save(self, *args, **kwargs):
        # Walidacja danych przed próbą zapisania
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title + " " + str(self.author)


class BookCopy(models.Model):
    cover_types = (
        ('brak informacji', 'brak informacji'),
        ('miękka', 'miękka'),
        ('twarda', 'twarda'),
    )
    year = models.IntegerField(default=2020)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    condition = models.CharField(max_length=100, default='brak informacji')
    cover = models.CharField(max_length=20, choices=cover_types,
                             default='brak informacji')

    def __str__(self):
        return self.book.title + " " + str(self.id)


class BorrowExtension(models.Model):
    days = models.IntegerField(default=0)
    extension_date = models.DateField(auto_now_add=True)


class Borrow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book_copy = models.ForeignKey(BookCopy, on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(default=None, null=True)
    borrow_extension = models.ForeignKey(BorrowExtension, on_delete=models.CASCADE, null=True, blank=True)

    def extend(self, days: int = 7):
        if self.borrow_extension is not None:
            raise ValidationError('Wypożycznie zostało już raz przedłużone')
        extension = BorrowExtension.objects.create(days=days)
        self.borrow_extension = extension
        return extension

    def return_book(self):
        self.return_date = datetime.date.today()
        self.save()

    def clean(self):
        if Borrow.objects.filter(book_copy=self.book_copy, return_date=None).exists() and self.return_date is None:
            raise ValidationError('Wypożyczono już tą książkę')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.book_copy) + " " + str(self.user)

