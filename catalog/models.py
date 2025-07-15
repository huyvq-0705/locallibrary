import uuid

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .constants import (
    GENRE_NAME_MAX_LENGTH,
    LANGUAGE_NAME_MAX_LENGTH,
    BOOK_TITLE_MAX_LENGTH,
    BOOK_SUMMARY_MAX_LENGTH,
    BOOK_ISBN_MAX_LENGTH,
    BOOKINSTANCE_IMPRINT_MAX_LENGTH,
    AUTHOR_FIRST_NAME_MAX_LENGTH,
    AUTHOR_LAST_NAME_MAX_LENGTH,
    LOAN_STATUS,
)


class Genre(models.Model):
    name = models.CharField(
        max_length=GENRE_NAME_MAX_LENGTH,
        help_text=_('Enter a book genre (e.g. Science Fiction)')
    )

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(
        max_length=LANGUAGE_NAME_MAX_LENGTH,
        help_text=_(
            "Enter the book's natural language (e.g. English, Vietnamese)")
    )

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=BOOK_TITLE_MAX_LENGTH)

    author = models.ForeignKey(
        'Author',
        on_delete=models.SET_NULL,
        null=True
    )

    summary = models.TextField(
        max_length=BOOK_SUMMARY_MAX_LENGTH,
        help_text=_('Enter a brief description of the book')
    )

    isbn = models.CharField(
        _('ISBN'),
        max_length=BOOK_ISBN_MAX_LENGTH,
        unique=True,
        help_text=_(
            '13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    )

    genre = models.ManyToManyField(
        'Genre',
        help_text=_('Select a genre for this book')
    )

    language = models.ForeignKey(
        'Language',
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])


class BookInstance(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text=_('Unique ID for this particular book across whole library')
    )
    book = models.ForeignKey('Book', on_delete=models.RESTRICT)
    imprint = models.CharField(max_length=BOOKINSTANCE_IMPRINT_MAX_LENGTH)
    due_back = models.DateField(null=True, blank=True)

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text=_('Book availability'),
    )

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        return f'{self.id} ({self.book.title})'


class Author(models.Model):
    first_name = models.CharField(max_length=AUTHOR_FIRST_NAME_MAX_LENGTH)
    last_name = models.CharField(max_length=AUTHOR_LAST_NAME_MAX_LENGTH)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField(_('Died'), null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'
