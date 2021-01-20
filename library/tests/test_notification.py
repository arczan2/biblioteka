from django.test import TestCase
from django.contrib.auth.models import User
from library.models import Borrow, BookCopy, Book, Notification
import datetime


class NotificationTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='Test_notify', email='test@test', password='test-test')
        self.book = Book.objects.create(title='Ksiazka notify', pages=250,)
        self.book_copy = BookCopy.objects.create(book=self.book)

    def test_if_notify_correctly(self):
        """
        Sprawdza czy system wysyła powiadomienia w poprawny sposób
        """
        borrow = Borrow.objects.create(user=self.user, book_copy=self.book_copy)
        borrow.borrow_date = datetime.date.today() - datetime.timedelta(days=26)
        borrow.save()
        Notification.notify()
        self.assertRaises(Notification.DoesNotExist,
                          Notification.objects.get,
                          user=self.user,
                          book_copy=self.book_copy)

        borrow.borrow_date = datetime.date.today() - datetime.timedelta(days=5)
        borrow.save()
        Notification.notify()
        notification = Notification.objects.get(user=self.user,
                                                book_copy=self.book_copy)
