from django.contrib import admin
from .models import Genre, Author, Book, BookCopy, Borrow, BorrowExtension
from .models import Notification


class BorrowAdmin(admin.ModelAdmin):
    list_filter = ['borrow_date', 'user']
    search_fields = ['user__username']


class BookCopyInline(admin.TabularInline):
    model = BookCopy
    extra = 0


class BookAdmin(admin.ModelAdmin):
    search_fields = ['title']
    inlines = [BookCopyInline]


admin.site.register(Genre)
admin.site.register(Author)
admin.site.register(Book, BookAdmin)
admin.site.register(BookCopy)
admin.site.register(Borrow, BorrowAdmin)
admin.site.register(BorrowExtension)
admin.site.register(Notification)
