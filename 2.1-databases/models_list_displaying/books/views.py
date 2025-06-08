from django.shortcuts import render

from books.models import Book
from django.utils.dateparse import parse_date


def books_view(request):
    template = 'books/books_list.html'
    books = Book.objects.all() # получаем книги из бд
    context = {'books': books}
    return render(request, template, context)

def books_by_date(request, pub_date):
    template = 'books/books_list.html'
    parsed_date = parse_date(pub_date)
    if not pub_date:
        return render(request, template, {'books': []}) # Если дата неверная

    books = Book.objects.filter(pub_date=parsed_date) # Получаем книги по дате публикации

    # Находим следующую и предыдущую книги по дате публикации
    next_book = Book.objects.filter(pub_date__gt=parsed_date).order_by('pub_date').first()
    previous_book = Book.objects.filter(pub_date__lt=parsed_date).order_by('pub_date').last()
    # Используем last для получения последней ранее опубликованной книги

    context = {
        'books': books,
        'next_book': next_book.pub_date.strftime('%Y-%m-%d') if next_book else None,
        'previous_book': previous_book.pub_date.strftime('%Y-%m-%d') if previous_book else None,
    }

    return render(request, template, context)

