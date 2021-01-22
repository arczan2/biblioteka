from operator import attrgetter
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.views import View
from django.shortcuts import render
from .models import Book, Borrow, BookCopy, Notification
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RegisterForm
from datetime import datetime
import operator


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
            return render(request, "library/index.html",
                          {"error": "Błędny login lub hasło"})


class LogoutView(View):
    """ Wylogowuje użytkownika """
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
                if name.lower() in book.title.lower():
                    books_list.append(book)
            books = books_list

        return render(request, 'library/books.html', {'books': books})


class BookDetailsView(View):
    """ Wyświetla informacje o książce """
    def get(self, request, id: int):
        book = Book.objects.get(pk=id)
        return render(request, 'library/book_details.html', {'book': book})


def home(request):
    return render(request, 'library/index.html')


def register(request):
    return render(request, 'library/registration.html')


@login_required
def ui_main(request):
    """ Panel użytkownika, wyświetla historię wypożyczeń """
    borrows = list(Borrow.objects.filter(user=request.user).order_by(
        "-return_date"))

    if len(borrows) <= 0:
        return render(request, 'library/borrows.html', {'borrows': borrows})
    i = 0
    # Przenieś nieoddane książki na początek
    while borrows[len(borrows) - 1].return_date is None and i < 3:
        borrows.insert(0, borrows.pop())
        i += 1
    # Oblicz dni do końca czasu wypożyczenia
    for borrow in borrows:
        deadline = datetime.now().date() - borrow.borrow_date
        borrow.days = -(deadline.days - 30)
        if borrow.return_date is not None:
            borrow.days = ''

    return render(request, 'library/borrows.html', {'borrows': borrows})


class RegistrationView(View):
    """ Dokonuje rejestracji użytkownika """
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()

        return render(request, 'library/registration.html',
                      {'form': RegisterForm})

    def get(self, request):
        form = RegisterForm
        return render(request, 'library/registration.html', {'form': form})


class UserBookListView(View):
    """ Wyświetla listę książek """
    def get(self, request):
        # Znajdź wszystkie książki
        books = Book.objects.all()
        name = None
        if 'search' in request.GET:
            name = request.GET['search']

        books_list = list()
        if name:
            for book in books:
                if name.lower() in book.title.lower():
                    books_list.append(book)
            books = books_list

        return render(request, 'library/user_books.html', {'books': books})


class UserBookDetailsView(View):
    """ Wyświetla informacje o książce """
    def get(self, request, id: int):
        user_borrow_count = Borrow.objects.filter(user=request.user,
                                                  return_date=None)
        book = Book.objects.get(pk=id)
        return render(request, 'library/user_book_details.html',
                      {'book': book, 'can_borrow': book.can_borrow(),
                       "user_borrow_count": len(user_borrow_count)})


class BorrowBookView(View):
    def get(self, request, id: int):
        book = Book.objects.get(pk=id)
        copies = BookCopy.objects.filter(book=book)
        book_copy = None
        for copy in copies:
            if len(Borrow.objects.filter(book_copy=copy,
                                         return_date=None)) == 0:
                book_copy = copy
                break
        Borrow.objects.create(user=request.user, book_copy=book_copy)
        return HttpResponseRedirect(reverse('library:uimain'))


@login_required
def notifications(request):
    notifications = Notification.objects.filter(
        user=request.user).order_by('-pk')
    return render(request, 'library/notifications.html',
                  {'notifications': notifications})


def genereate_notification(request):
    """Wejście na ten adres uruchamia system powiadomień"""
    Notification.notify()
    return HttpResponse('Wysłano powiadomienia')


def read_notifictaion(request, id: int):
    """Oznacza powiadomienie jako przeczytane"""
    notification = Notification.objects.get(pk=id)
    notification.read = True
    notification.save()
    return HttpResponseRedirect(reverse('library:notifications'))


class SettingsView(View):
    """ Umożliwia zmianę hasła """
    def get(self, request):
        """ Wyświetla formularz zmiany hasła """
        return render(request, 'library/settings.html')

    def post(self, request):
        """ Przetwarza formularz zmiany hasła """
        # Pobierz hasła
        password = request.POST['CurrentPassword']
        password1 = request.POST['NewPassword']
        password2 = request.POST['ValidNewPassword']
        # Wyszukanie użytkownika o podanych danych logowania
        if request.user.check_password(password) and password1 == password2:
            # Zmiana hasła
            request.user.set_password(password1)
            request.user.save()
            return render(request, "library/settings.html",
                          {"error": "Hasło zostało zmienione"})
        else:
            return render(request, "library/settings.html",
                          {"error": "Próba nie udana"})
