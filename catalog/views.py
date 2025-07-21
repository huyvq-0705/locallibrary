from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from catalog.models import Book, Author, BookInstance
from catalog.constants import LOAN_STATUS_AVAILABLE, LOAN_STATUS_ON_LOAN, PAGINATION_BY
from catalog.constants import LOAN_STATUS


def index(request):

    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()
    num_instances_available = BookInstance.objects.filter(
        status__exact=LOAN_STATUS_AVAILABLE
    ).count()
    num_authors = Author.objects.count()

    num_visits = request.session.get('num_visits', 0) + 1
    request.session['num_visits'] = num_visits

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }

    return render(request, 'index.html', context)


class BookListView(generic.ListView):
    model = Book
    context_object_name = 'book_list'
    template_name = 'catalog/book_list.html'
    paginate_by = PAGINATION_BY 


class BookDetailView(generic.DetailView):
    model = Book
    context_object_name = 'book'
    template_name = 'catalog/book_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        context['genres'] = book.genre.all()
        context['instances'] = book.bookinstance_set.all()
        return context


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = PAGINATION_BY 

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user, status__exact=LOAN_STATUS_ON_LOAN).order_by('due_back')
