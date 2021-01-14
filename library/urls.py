from django.urls import path

from . import views

app_name = 'library'

urlpatterns = [
    path('', views.home, name='frontpage'),
    path('books', views.book, name='books'),
    path('registration', views.register, name='registration'),
    path('uimain', views.ui_main, name='uimain')
]
