from django.test import TestCase
from django.contrib.auth.models import User
from library.models import Borrow, BookCopy, Book


class BookTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='Test2', email='test@test', password='test-test')

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

    def test_if_book_return_correct_borrow_state(self):
        """
        Sprawdza czy książka zwraca poprawną informację o tym czy
        jest możliwe jej wypożyczenie
        """
        book = Book.objects.create(title='Ksiazka9', pages=250)
        book_copy = BookCopy.objects.create(book=book)
        self.assertTrue(book.can_borrow())
        borrow = Borrow.objects.create(user=self.user, book_copy=book_copy)
        self.assertFalse(book.can_borrow())
