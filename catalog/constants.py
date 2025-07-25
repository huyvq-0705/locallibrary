from django.utils.translation import gettext_lazy as _

GENRE_NAME_MAX_LENGTH = 200
LANGUAGE_NAME_MAX_LENGTH = 200
BOOK_TITLE_MAX_LENGTH = 200
BOOK_SUMMARY_MAX_LENGTH = 1000
BOOK_ISBN_MAX_LENGTH = 13
BOOKINSTANCE_IMPRINT_MAX_LENGTH = 200
AUTHOR_FIRST_NAME_MAX_LENGTH = 100
AUTHOR_LAST_NAME_MAX_LENGTH = 100
LOAN_STATUS_MAINTENANCE = 'm'
LOAN_STATUS_ON_LOAN = 'o'
LOAN_STATUS_AVAILABLE = 'a'
LOAN_STATUS_RESERVED = 'r'
DEFAULT_RENEWAL_WEEKS = 3
PAGINATION_BY = 10
PERM_MARK_RETURNED = 'catalog.can_mark_returned'
PERM_ADD_AUTHOR = 'catalog.add_author'
PERM_CHANGE_AUTHOR = 'catalog.change_author'
PERM_DELETE_AUTHOR = 'catalog.delete_author'
DEFAULT_DATE_OF_DEATH = '2000-01-01'

LOAN_STATUS = (
    (LOAN_STATUS_MAINTENANCE, 'Maintenance'),
    (LOAN_STATUS_ON_LOAN, 'On loan'),
    (LOAN_STATUS_AVAILABLE, 'Available'),
    (LOAN_STATUS_RESERVED, 'Reserved'),
)

ISBN_HELP_TEXT = _(
    '13 Character '
    '<a href="https://www.isbn-international.org/content/what-isbn">'
    'ISBN number'
    '</a>'
)
