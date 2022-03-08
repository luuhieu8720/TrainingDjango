from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Book, Author, BookInstance, Genre
from . import constants

def index(request):
    num_books = Book.objects.count()

    num_instances = BookInstance.objects.count()

    num_instances_available = BookInstance.objects.filter(status__exact=constants.BOOK_STATUS_AVAILABLE).count()

    num_authors = Author.objects.count()

    num_genres = Genre.objects.filter(name__exact= constants.GENRE_NAME).count()

    num_visits = request.session.get('num_visits', constants.NUM_VISITS_INITIAL)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'num_visits': num_visits,
    }

    return render(request, 'index.html', context=context)

class BookListView(generic.ListView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author

class BookDetailView(generic.DetailView):
    model = Book
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["book_genres"] = context["book"].genre.all()
        context["book_instances"] = context["book"].bookinstance_set.all()
        return context

class AuthorDetailView(generic.DetailView):
    model = Author

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = constants.PAGINATE

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
