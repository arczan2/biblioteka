from django.urls import path

from . import views

app_name = 'library'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login', views.LoginView.as_view(), name='login'),
    path('books', views.BookListView.as_view(), name='books'),
    path('book/<int:book_id>', views.BookDetails.as_view(),
         name='book_details'),
    path('', views.home, name='frontpage'),
    path('books', views.book, name='books'),
    path('registration', views.register, name='registration'),
    path('uimain', views.ui_main, name='uimain')
]
