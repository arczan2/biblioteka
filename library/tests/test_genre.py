from django.test import TestCase
from library.models import Genre


class GenreTestCase(TestCase):
    def test_cant_add_two_genres_with_same_name(self):
        """
        Sprawdza czy próba dodania dwóch gatunków o tej samej nazwie wywoła
        wyjątek
        """
        Genre.objects.create(name='Thriller', description='Opis 1')
        self.assertRaises(Exception, Genre.objects.create,
                          name='thriller', description='Opis 3')

    def test_default_description(self):
        """
        Sprawdza czy jeżeli nie podano opisu to zostanie ustawiony "brak opisu"
        """
        genre = Genre.objects.create(name='Horror')
        self.assertEqual(genre.description, 'brak opisu')

    def test_cant_add_genre_without_or_with_empty_name(self):
        """
        Sprawdza czy próby dodania gatunku bez nazwy zostanie zablokowana
        """
        self.assertRaises(Exception, Genre.objects.create, name='')
        self.assertRaises(Exception, Genre.objects.create)
