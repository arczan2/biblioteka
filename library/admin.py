from django.contrib import admin
from .models import Genre, Author, Book, BookCopy, Borrow, BorrowExtension
from .models import Notification


admin.site.register(Genre)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(BookCopy)
admin.site.register(Borrow)
admin.site.register(BorrowExtension)
admin.site.register(Notification)
