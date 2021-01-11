from django.views.generic import TemplateView
from django.views import View
from django.shortcuts import render
from .models import Book


class IndexView(TemplateView):
    """ Wyświetla stronę główną """
    template_name = "library/index.html"


class BookListView(View):
    """ Wyświetla listę książek """
    def get(self, request):
        books = Book.objects.all()
        return render(request, 'library/books.html', {'books': books})
