from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from . import constants

def index(request):
    num_books = Book.objects.count()

    num_instances = BookInstance.objects.count()

    num_instances_available = BookInstance.objects.filter(status__exact=constants.BOOK_STATUS_AVAILABLE).count()

    num_authors = Author.objects.count()

    num_genres = Genre.objects.filter(name__exact= constants.GENRE_NAME).count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres
    }

    return render(request, 'index.html', context=context)
