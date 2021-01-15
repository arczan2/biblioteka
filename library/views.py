from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.views import View
from django.shortcuts import render
from .models import Book, Borrow
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RegisterForm


class LoginView(View):
    """ Logowanie użytkownika """
    def post(self, request):
        # Pobierz dane logowania
        username = request.POST['username']
        password = request.POST['password']
        # Wyszukanie użytkownika o podanych danych logowania
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Zaloguj użytkownika
            login(request, user)
            return HttpResponseRedirect(reverse('library:uimain'))
        else:
            return HttpResponseRedirect(reverse('library:frontpage'))


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('library:frontpage'))


class IndexView(TemplateView):
    """ Wyświetla stronę główną """
    template_name = "library/index.html"


class BookListView(View):
    """ Wyświetla listę książek """
    def get(self, request):
        books = Book.objects.all()
        name = None
        if 'search' in request.GET:
            name = request.GET['search']

        books_list = list()
        if name:
            for book in books:
                if name in book.title:
                    books_list.append(book)
            books = books_list

        return render(request, 'library/books.html', {'books': books})


class BookDetailsView(View):
    """ Wyświetla informacje o książce """
    def get(self, request, id: int):
        book = Book.objects.get(pk=id)
        return render(request, 'library/book_details.html', {'book': book})


class MyBorrowList(View):
    pass


def home(request):
    return render(request, 'library/index.html')


def register(request):
    return render(request, 'library/registration.html')


@login_required
def ui_main(request):
    borrows = Borrow.objects.all()
    return render(request, 'library/borrows.html', {'borrows': borrows})


class RegistrationView(View):
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()

        return render(request, 'library/registration.html', {'form': RegisterForm})

    def get(self, request):
        form = RegisterForm
        return render(request, 'library/registration.html', {'form': form})
