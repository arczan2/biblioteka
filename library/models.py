from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from enum import Enum
import datetime
from django.utils import timezone


class Genre(models.Model):
    """
    Klasa reprezentuje gatunek książki

    Attributes
    ----------
    name : str
        Nazwa gatunku(np. "Horror")
    description : str
        Opis
    """
    name = models.CharField(max_length=20, unique=True, null=False, blank=False,
                            verbose_name="Gatunek")
    description = models.TextField(default='brak opisu', verbose_name="Opis")

    class Meta:
        verbose_name = 'Gatunek'
        verbose_name_plural = 'Gatunki'

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
    """
    Klasa reprezentuje autora książek

    Attributes
    ----------
    name : str
        Imię
    surname : str
        Nazwisko
    nationality : str
        Narodowość
    """
    name = models.CharField(max_length=40, null=False, verbose_name="Imię")
    surname = models.CharField(max_length=40, null=False,
                               verbose_name="Nazwisko")
    nationality = models.TextField(max_length=50, default='narodowosc nieznana',
                                   verbose_name="Narodowość")

    class Meta:
        verbose_name = 'Autora'
        verbose_name_plural = 'Autorzy'

    def clean(self):
        from django.core.exceptions import ValidationError

        if self.name is None or self.name == '' or self.surname is None or self.surname == '':
            raise ValidationError('Imię i nazwisko to pola wymagane i nie mogą byc puste')

        if self.name.lower() in [names['name'].lower() for names in
            Author.objects.all().values('name')] and self.surname.lower() in [surnames['surrname'].lower() for surnames in
            Author.objects.all().values('surname')] and self.nationality.lower() in [nationalities['nationality'].lower() for nationalities in
            Author.objects.all().values('nationality')]:
                raise ValidationError('Taka osoba już istnieje w bazie autorów')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name + " " + self.surname


class Book(models.Model):
    """
    Klasa reprezentuje książkę

    Attributes
    ----------
    title : str
        Tytuł
    pages : int
        Liczba stron
    genre : Genre
        Gatunek książki
    author : Author
        Gatunek książki
    description : str
        Opis
    image : Image
        Zdjęcie okładki
    """
    title = models.CharField(max_length=40, verbose_name="Tytuł")
    pages = models.IntegerField(verbose_name="Ilość stron")
    genre = models.ForeignKey(Genre, null=True, on_delete=models.SET_NULL,
                              blank=True, verbose_name="Gatunek")
    author = models.ForeignKey(Author, null=True, on_delete=models.SET_NULL,
                               blank=True, verbose_name="Autor")
    description = models.TextField(default='brak opisu', verbose_name="Opis")
    image = models.ImageField(upload_to='book_images/', null=True, blank=True,
                              verbose_name="Ilustracja okładki")

    class Meta:
        verbose_name = 'Książka'
        verbose_name_plural = 'Książki'

    def clean(self):
        from django.core.exceptions import ValidationError
        # Jeżeli tytul książki jest pusta to zwróć wyjątek
        if self.title is None or self.title == '':
            raise ValidationError('Tytul ksiazki nie moze być pusta')
        # Sprawdz czy ksiazka o tem tytule juz istnieje w bazie
        if self.title.lower() in [titles['title'].lower() for titles in
                                 Book.objects.all().values('title')]:
            if Book.objects.get(title=self.title) != self:
                raise ValidationError('Ksiazka o tym tytule juz istnieje')

    def save(self, *args, **kwargs):
        # Walidacja danych przed próbą zapisania
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title + " " + str(self.author)

    def can_borrow(self):
        """
        Zwraca prawdę gdy są dostępne egzemplarze książkij
        """
        book_copies = BookCopy.objects.filter(book=self)

        try:
            for copy in book_copies:
                borrows = Borrow.objects.get(book_copy=copy, return_date=None)
        except Borrow.DoesNotExist:
            return True

        return False


class BookCopy(models.Model):
    """
    Klasa reprezentuje egzemplarz książki

    Attributes
    ----------
    year : int
        Rok wydania
    book : Book
        Książka której kopią jest dany egzemplarz
    condition : str
        Stan egzemplarza, dowolny opis(np. "Lekko naderwana okładka")
    cover : str
        Typ oprawy(do wyboru z cover_types)
    """
    cover_types = (
        ('brak informacji', 'brak informacji'),
        ('miękka', 'miękka'),
        ('twarda', 'twarda'),
    )
    year = models.IntegerField(default=2020, verbose_name="Rok wydania")
    book = models.ForeignKey(Book, on_delete=models.CASCADE,
                             verbose_name="Książka")
    condition = models.CharField(max_length=100, default='brak informacji',
                                 verbose_name="Stan książki")
    cover = models.CharField(max_length=20, choices=cover_types,
                             default='brak informacji',
                             verbose_name="Typ okładki")

    class Meta:
        verbose_name = 'Egzemplarz książki'
        verbose_name_plural = 'Egzemplarze książek'

    def __str__(self):
        return self.book.title + " " + str(self.id)


class Borrow(models.Model):
    """
    Klasa reprezentuje wypożyczenie książki przez czytelnika

    Attributes
    ----------
    user : User
        Użytkownik, który wypożyczył książkę
    book_copy : BookCopy
        Wypożyczony egzemplarz
    borrow_date : datetime.date
        Data wypożyczenia
    return_date : datetime.date
        Data oddania
    cover : str
        Typ oprawy(do wyboru z cover_types)
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name="Użytkownik")
    book_copy = models.ForeignKey(BookCopy, on_delete=models.CASCADE,
                                  verbose_name="Egzemplarz książki")
    borrow_date = models.DateField(default=None, null=False,
                                   verbose_name="Data wypożyczenia")
    return_date = models.DateField(default=None, null=True, blank=True,
                                   verbose_name="Data oddania")

    class Meta:
        verbose_name = 'Wypożyczenie'
        verbose_name_plural = 'Wypożyczenia'

    def return_book(self) -> None:
        self.return_date = datetime.date.today()
        self.save()

    def clean(self):
        if Borrow.objects.filter(book_copy=self.book_copy, return_date=None)\
                .exists() and self.return_date is None:
            if Borrow.objects.get(book_copy=self.book_copy,
                                  return_date=None) != self:
                raise ValidationError('Wypożyczono już tą książkę')

    def save(self, *args, **kwargs):
        if not self.id:
            self.borrow_date = datetime.date.today()
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.book_copy) + " " + str(self.user)


class Notification(models.Model):
    """
    Klasa reprezentuje powiadomienie

    Attributes
    ----------
    user : User
        Użytkownik, do którego skierowane jest powiadomienie
    book_copy : BookCopy
        Egzemplarz książki, którego dodtyczy wypożyczenie
    date : datetime.date
        Data wysłania
    message : str
        Treść powiadomienia
    read : bool
        Czy powiadomienie zostało odczytane?
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='Użytkownik')
    book_copy = models.ForeignKey(BookCopy, on_delete=models.CASCADE,
                                  verbose_name="Egzemplarz książki")
    date = models.DateField(auto_now_add=True, verbose_name="Data")
    message = models.TextField(default='', verbose_name="Wiadomość")
    read = models.BooleanField(default=False, verbose_name="Czy odczytano?")

    class Meta:
        verbose_name = 'Powiadomienie'
        verbose_name_plural = 'Powiadomienia'

    def __str__(self):
        return "{} - {} - {}".format(self.user.username, self.date,
                                     self.message)

    @classmethod
    def notify(cls) -> None:
        today_date = datetime.date.today()

        borrows = Borrow.objects.filter(return_date=None)
        for borrow in borrows:
            if (today_date - borrow.borrow_date).days in (23, 27, 28):
                message = "Zostały ci {} dni do oddania książki {}".format(
                    30 - (today_date - borrow.borrow_date).days,
                    borrow.book_copy.book.title
                )
                cls.objects.create(user=borrow.user, book_copy=borrow.book_copy,
                                   message=message)
            elif (today_date - borrow.borrow_date).days == 29:
                message = "Jutro musisz oddać {}".format(
                    borrow.book_copy.book.title
                )
                cls.objects.create(user=borrow.user, book_copy=borrow.book_copy,
                                   message=message)
            elif (today_date - borrow.borrow_date).days == 30:
                message = "Dzisiaj musisz oddać książkę {}!".format(
                    borrow.book_copy.book.title
                )
                cls.objects.create(user=borrow.user, book_copy=borrow.book_copy,
                                   message=message)
            elif (today_date - borrow.borrow_date).days > 30:
                message = "Spóźniasz się {} dni z oddaniem książki {}".format(
                    (today_date - borrow.borrow_date).days - 30,
                    borrow.book_copy.book.title
                )
                cls.objects.create(user=borrow.user, book_copy=borrow.book_copy,
                                   message=message)
