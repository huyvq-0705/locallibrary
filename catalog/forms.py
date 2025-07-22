import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from catalog.models import BookInstance

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(
        help_text=_("Enter a date between today and 4 weeks (default 3)."),
        widget=forms.TextInput(attrs={'type': 'date'})
    )
    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date – renewal in past'))
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date – more than 4 weeks ahead'))
        return data

class RenewBookModelForm(forms.ModelForm):
    class Meta:
        model = BookInstance
        fields = ['due_back']
        labels = {'due_back': _('Renewal date')}
        help_texts = {'due_back': _('Enter a date between today and 4 weeks (default 3).')}
    def clean_due_back(self):
        data = self.cleaned_data['due_back']
        # same validations…
        return data
