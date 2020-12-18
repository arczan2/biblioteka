from django.test import TestCase
from django.contrib.auth.models import User
from library.models import Borrow, BookCopy, Book


class BorrowTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='Test', email='test@test', password='test-test')
        self.book = Book.objects.create(title='Ksiazka', pages=250,)
        self.book_copy = BookCopy.objects.create(book=self.book)

    def test_if_can_borrow(self):
        """
        Sprawdza czy można wypożyczyć książkę
        """
        Borrow.objects.create(user=self.user, book_copy=self.book_copy)
