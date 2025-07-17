from django import template
from catalog.constants import LOAN_STATUS_AVAILABLE, LOAN_STATUS_MAINTENANCE

register = template.Library()


@register.simple_tag
def get_status_class(status):
    if status == LOAN_STATUS_AVAILABLE:
        return "text-success"
    elif status == LOAN_STATUS_MAINTENANCE:
        return "text-danger"
    else:
        return "text-warning"
