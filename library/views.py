from django.views.generic import TemplateView
from django.views import View
from django.shortcuts import render
from .models import Book
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse


class LoginView(View):
    """ Logowanie użytkownika """
    def get(self, request):
        # Pobierz dane logowania
        username = request.POST['username']
        password = request.POST['password']
        # Wyszukanie użytkownika o podanych danych logowania
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Zaloguj użytkownika
            login(request, user)
            return HttpResponseRedirect(reverse('library:books'))
        else:
            return HttpResponseRedirect(reverse('library:index'))


class IndexView(TemplateView):
    """ Wyświetla stronę główną """
    template_name = "library/index.html"


class BookListView(View):
    """ Wyświetla listę książek """
    def get(self, request):
        books = Book.objects.all()
        return render(request, 'library/books.html', {'books': books})


class BookDetails(View):
    """ Wyświetla informacje o książce """
    def get(self, request, book_id: int):
        book = Book.objects.get(pk=book_id)
        return render(request, 'library/book_details.html', {'book': book})


class MyBorrowList(View):
    pass
