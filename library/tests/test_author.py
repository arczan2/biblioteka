from django.test import TestCase
from library.models import Author, Book


class AuthorTestCase(TestCase):

    def test_cant_add_an_existing_author(self):
        """
         Sprawdza czy dodanie identycznego akrota zwróci wyjątek
        """
        Author.objects.create(name='Adam', surrname='Mickiewicz',
                              nationality='Polska')
        self.assertRaises(Exception, Author.objects.create,name='Adam',
                          surrname='Mickiewicz', nationality='Polska')

    def test_cant_add_author_without_name(self):
        """
         Sprawdza czy powiedzie się próba dodania osoby bez imienia
        """
        self.assertRaises(Exception, Author.objects.create,
                          surrname="Sapkowski", nationality='Polska')

    def test_cant_add_author_without_surrname(self):
        """
        Sprawdza czy powiedzie się próba dodania osoby bez imienia
        """
        self.assertRaises(Exception, Author.objects.create, name="Andrzej",
                          nationality='Polska')

    def test_delete_author(self):
        """
        Sprawdza czy po usunięciu autora, książki do niego przypisane nie
        zostaną usunięte i czy ich relacja do autora zostanie ustawiona na 
        None
        """
        author = Author.objects.create(name='Arek', surrname='Darek',
                                       nationality='USA')
        book = Book.objects.create(title='Book1', pages=333, author=author)
        self.assertEqual(book.author, author)
        Author.objects.filter(name='Arek').delete()
        book = Book.objects.get(title='Book1')
        self.assertEqual(book.author, None)
