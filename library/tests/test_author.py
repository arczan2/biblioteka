from django.test import TestCase
from library.models import Author

class AuthorTestCase(TestCase):

    #Sprawdza czy dodanie identycznego akrota zwróci wyjątek
    def  test_cant_add_an_existing_author(self):
        Author.objects.create(name='Adam', surrname='Mickiewicz', nationality='Polska')
        self.assertRaises(Exception, Author.objects.create,name='Adam', surrname='Mickiewicz', nationality='Polska')

    #Sporawdza czy powiedzie się próba dodania osoby bez imienia
    def test_cant_add_author_without_name(self):
        self.assertRaises(Exception, Author.objects.create, surrname="Sapkowski", nationality='Polska')

    #Sporawdza czy powiedzie się próba dodania osoby bez imienia
    def test_cant_add_author_without_surrname(self):
        self.assertRaises(Exception, Author.objects.create, name="Andrzej", nationality='Polska')