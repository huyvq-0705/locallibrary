from datetime import (
    date,
    timedelta
)


from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views import generic
from django.urls import reverse_lazy
from django.views.generic.edit import (
    UpdateView,
    CreateView,
    DeleteView
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)

from catalog.models import (
    Book,
    Author,
    BookInstance
)
from catalog.constants import (
    LOAN_STATUS_AVAILABLE,
    LOAN_STATUS_ON_LOAN,
    DEFAULT_RENEWAL_WEEKS,
    PAGINATION_BY,
    DEFAULT_DATE_OF_DEATH
)
from catalog.forms import RenewBookModelForm


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
        return BookInstance.objects.filter(
            borrower=self.request.user, status__exact=LOAN_STATUS_ON_LOAN).order_by('due_back')


class BookRenewView(PermissionRequiredMixin, UpdateView):
    # Sử dụng Class-Based View (UpdateView) thay vì Function-Based View
    model = BookInstance
    form_class = RenewBookModelForm
    context_object_name = 'book_instance'
    template_name = 'catalog/book_renew_librarian.html'
    permission_required = 'catalog.can_mark_returned'
    success_url = reverse_lazy('my-borrowed')

    def get_initial(self):
        # propose a date DEFAULT_RENEWAL_WEEKS weeks from today
        return {
            'due_back': date.today() + timedelta(weeks=DEFAULT_RENEWAL_WEEKS)
        }


class AuthorListView(generic.ListView):
    model = Author
    template_name = 'catalog/author_list.html'
    context_object_name = 'author_list'
    paginate_by = PAGINATION_BY


class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'catalog/author_detail.html'


class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    permission_required = 'catalog.add_author'
    initial = {'date_of_death': DEFAULT_DATE_OF_DEATH}


class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    permission_required = 'catalog.change_author'


class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    permission_required = 'catalog.delete_author'
    success_url = reverse_lazy('author-list')


class LoanedBooksAllListView(PermissionRequiredMixin, generic.ListView):
    model = BookInstance
    permission_required = 'catalog.can_mark_returned'
    template_name = 'catalog/bookinstance_list_borrowed_all.html'
    paginate_by = PAGINATION_BY

    def get_queryset(self):
        return BookInstance.objects.filter(
            status__exact=LOAN_STATUS_ON_LOAN
        ).order_by('due_back')
