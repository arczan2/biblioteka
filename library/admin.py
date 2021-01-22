from django.contrib import admin
from .models import Genre, Author, Book, BookCopy, Borrow
from .models import Notification


class BorrowAdmin(admin.ModelAdmin):
    list_filter = ['borrow_date', 'user']
    search_fields = ['user__username']
    list_display = ('book_copy', 'user', 'borrow_date', 'return_date',)


class BookCopyInline(admin.TabularInline):
    model = BookCopy
    extra = 0


class BookAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_display = ('title', 'genre', 'author', )
    inlines = [BookCopyInline]


class BookCopyAdmin(admin.ModelAdmin):
    list_display = ('book', 'id')


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('message', 'user', 'date')


admin.site.register(Genre)
admin.site.register(Author)
admin.site.register(Book, BookAdmin)
admin.site.register(BookCopy, BookCopyAdmin)
admin.site.register(Borrow, BorrowAdmin)
admin.site.register(Notification, NotificationAdmin)
