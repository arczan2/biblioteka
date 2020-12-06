from django.test import TestCase
from library.models import Author


class AuthorTestCase(TestCase):

    def test_cant_add_an_existing_author(self):
        """
         Sprawdza czy dodanie identycznego akrota zwróci wyjątek
        """
        Author.objects.create(name='Adam', surrname='Mickiewicz', nationality='Polska')
        self.assertRaises(Exception, Author.objects.create,name='Adam', surrname='Mickiewicz', nationality='Polska')

    def test_cant_add_author_without_name(self):
        """
         Sporawdza czy powiedzie się próba dodania osoby bez imienia
        """
        self.assertRaises(Exception, Author.objects.create, surrname="Sapkowski", nationality='Polska')


    def test_cant_add_author_without_surrname(self):
        """
        Sporawdza czy powiedzie się próba dodania osoby bez imienia
        """
        self.assertRaises(Exception, Author.objects.create, name="Andrzej", nationality='Polska')