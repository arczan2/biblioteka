from django.test import TestCase
from library.models import BookCopy, Book


class BookTestCase(TestCase):
    def setUp(self):
        self.book = Book.objects.create(title="Test", pages=250)

    def test_cant_add_book_copy_without_book_attached(self):
        """
        Sprawdza czy próba dodania egzemparza książki bez podania jakiej ksiązki
        jest to egzemplarz
        """
        self.assertRaises(Exception, BookCopy.objects.create)

    def test_can_add_multiple_copies_to_one_book(self):
        first_copy = BookCopy.objects.create(book=self.book)
        second_copy = BookCopy.objects.create(book=self.book)
        self.assertEqual(first_copy.book, self.book)
        self.assertEqual(second_copy.book, self.book)

    def test_delete_book_copy_when_book_is_deleted(self):
        new_book = Book.objects.create(title='Do usuniecia', pages=250)
        copy_id = BookCopy.objects.create(book=new_book).id
        BookCopy.objects.get(id=copy_id)
        new_book.delete()
        self.assertRaises(BookCopy.DoesNotExist,
                          BookCopy.objects.get, id=copy_id)

    def test_check_default_values(self):
        copy = BookCopy.objects.create(book=self.book)
        self.assertEqual(copy.year, 2020)
        self.assertEqual(copy.condition, 'brak informacji')
        self.assertEqual(copy.cover, 'brak informacji')