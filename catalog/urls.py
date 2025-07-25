# catalog/urls.py
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # <- route chính của /catalog/
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path(
        'mybooks/',
        views.LoanedBooksByUserListView.as_view(),
        name='my-borrowed'),
    path(
        'book/<uuid:pk>/renew/',
        views.BookRenewView.as_view(),
        name='renew-book'),
    path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
    path(
        'author/<int:pk>/update/',
        views.AuthorUpdate.as_view(),
        name='author-update'),
    path(
        'author/<int:pk>/delete/',
        views.AuthorDelete.as_view(),
        name='author-delete'),
    path(
        'borrowed/',
        views.LoanedBooksAllListView.as_view(),
        name='all-borrowed'),
    path('authors/', views.AuthorListView.as_view(), name='author-list'),
    path(
        'author/<int:pk>/',
        views.AuthorDetailView.as_view(),
        name='author-detail'),
]
