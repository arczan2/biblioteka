from django.urls import path

from . import views

app_name = 'library'

urlpatterns = [
    path('login', views.LoginView.as_view(), name='login'),
    path('', views.home, name='frontpage'),
    path('books', views.BookListView.as_view(), name='books'),
    path('book/<int:id>', views.BookDetailsView.as_view(), name='book_details'),
    path('uimain', views.ui_main, name='uimain'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('registration', views.RegistrationView.as_view(), name='registration'),
]
