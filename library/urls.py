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
    path('user_books', views.UserBookListView.as_view(), name='userbooks'),
    path('user_book/<int:id>', views.UserBookDetailsView.as_view(),
         name='user_book_details'),
    path('book/borrow/<int:id>', views.BorrowBookView.as_view(),
         name='borrow_book'),
    path('dev/notificate', views.genereate_notification,
         name='dev_generate_notifications'),
    path('read_notification/<int:id>', views.read_notifictaion,
         name='read_notification'),
    path('settings', views.SettingsView.as_view(), name='settings'),
]
