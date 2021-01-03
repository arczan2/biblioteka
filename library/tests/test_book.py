from django.test import TestCase
from library.models import Book


class BookTestCase(TestCase):
    def test_cant_add_two_books_with_same_name(self):
        """
        Sprawdza czy próba dodania dwóch książek o tej samej nazwie wywoła
        wyjątek
        """
        Book.objects.create(title='Ksiazka', pages=250)
        self.assertRaises(Exception, Book.objects.create,
                          title='ksiazka', pages=300)

    def test_cant_add_book_without_number_of_pages(self):
        """
        Sprawdza czy próby dodania ksiazki bez stron zostaną zablokowane
        """
        self.assertRaises(Exception, Book.objects.create, pages=None)
        self.assertRaises(Exception, Book.objects.create)

    def test_cant_add_book_without_title(self):
        """
        Sprawdza czy próby dodania ksiazki bez tytulu zostanie zablokowana
        """
        self.assertRaises(Exception, Book.objects.create, name=None)
        self.assertRaises(Exception, Book.objects.create)
