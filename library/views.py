from django.shortcuts import render
from django.shortcuts import redirect


def home(request):
    return render(request, 'library/index.html')


def book(request):
    return render(request, 'library/books.html')


def register(request):
    return render(request, 'library/registration.html')



def ui_main(request):
    return render(request, 'library/ui_main.html')