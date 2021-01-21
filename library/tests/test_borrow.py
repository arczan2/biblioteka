from django.test import TestCase
from django.contrib.auth.models import User
from library.models import Borrow, BookCopy, Book
from django.core.exceptions import ValidationError
import datetime


class BorrowTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='Test', email='test@test', password='test-test')
        self.book = Book.objects.create(title='Ksiazka', pages=250,)
        self.book_copy = BookCopy.objects.create(book=self.book)
        self.book_copy2 = BookCopy.objects.create(book=self.book)
        self.book_copy3 = BookCopy.objects.create(book=self.book)

    def test_if_can_borrow(self):
        """
        Sprawdza czy można wypożyczyć książkę
        """
        borrow = Borrow.objects.create(user=self.user, book_copy=self.book_copy)
        self.assertEqual(borrow.borrow_date, datetime.date.today())
        self.assertEqual(borrow.return_date, None)

    def test_if_can_return(self):
        """
        Sprawdza czy poprawnnie oznacza oddane książki
        """
        return_book = Borrow.objects.create(user=self.user, book_copy=self.book_copy2)
        return_book.return_book()
        ID = return_book.id
        self.assertEqual(Borrow.objects.get(id=ID).return_date, datetime.date.today())

    def test_if_cant_borrow_same_book_twice(self):
        """
        Sprawdza czy nie można wypożyczyć tej samej książki podwójnie
        """
        Borrow.objects.create(user=self.user, book_copy=self.book_copy3)
        self.assertRaises(ValidationError, Borrow.objects.create, user=self.user, book_copy=self.book_copy3)
