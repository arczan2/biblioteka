from django.test import TestCase
from library.models import Genre, Book


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

    def test_delete_genre(self):
        """
        Sprawdza czy po usunięciu gatunku, książki do niego przypisane nie
        zostaną usunięte i czy ich relacja do gatunku zostanie ustawiona na 
        None
        """
        genre = Genre.objects.create(name='Dramat', description='...')
        book = Book.objects.create(title='Book2', pages=333, genre=genre)
        self.assertEqual(book.genre, genre)
        Genre.objects.filter(name='Dramat').delete()
        book = Book.objects.get(title='Book2')
        self.assertEqual(book.genre, None)
