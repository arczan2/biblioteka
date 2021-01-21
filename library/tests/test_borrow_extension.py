import datetime

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth.models import User
from library.models import Borrow, BookCopy, Book,BorrowExtension


class BorrowTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='Test_ext', email='test_ext@test', password='test-test')
        self.book = Book.objects.create(title='Ksiazka_ext', pages=250, )
        self.book_copy = BookCopy.objects.create(book=self.book)
        self.book_copy2 = BookCopy.objects.create(book=self.book)
        self.book_copy3 = BookCopy.objects.create(book=self.book)
        self.borrow1 = Borrow.objects.create(user=self.user,
                                             book_copy=self.book_copy)
        self.borrow2 = Borrow.objects.create(user=self.user,
                                             book_copy=self.book_copy2)

    def test_if_can_extend_borrow(self):
        extension = self.borrow1.extend(4)
        self.assertEqual(extension.days, 4)
        self.assertEqual(self.borrow1.borrow_extension, extension)
        self.assertEqual(extension.extension_date, datetime.date.today())

    def test_if_can_extend_twice(self):
        self.borrow2.extend()
        self.assertRaises(ValidationError, self.borrow2.extend)
