from django.db import models


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

    def save(self, *args, **kwargs):
        # Walidacja danych przed próbą zapisania
        self.clean()
        super().save(*args, **kwargs)


class Book(models.Model):
    title = models.CharField(max_length=40)
    pages = models.IntegerField()
    #genre
    #author

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
