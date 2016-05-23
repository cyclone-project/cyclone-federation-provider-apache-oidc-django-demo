import os
import sys
from django import forms
from django.utils.translation import ugettext_lazy as _

from oidc_customization.models import MyUser


class PopoverForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(PopoverForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            help_text = self.fields[field].help_text
            self.fields[field].help_text = None
            if help_text == '':
                help_text = self.fields[field].widget.attrs.get("placeholder", "")
            if help_text != '':
                self.fields[field].widget.attrs.update(
                    {'class': 'has-popover', 'data-content': help_text, 'data-placement': 'top',
                     'data-container': 'body', 'data-html': "true"})


class PopoverModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PopoverModelForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            help_text = self.fields[field].help_text
            self.fields[field].help_text = None
            if help_text == '':
                help_text = self.fields[field].widget.attrs.get("placeholder", "")
            if help_text != '':
                self.fields[field].widget.attrs.update(
                    {'class': 'has-popover', 'data-content': help_text, 'data-placement': 'top',
                     'data-container': 'body', 'data-html': "true"})


class RegisterUserFromOIDC(PopoverModelForm):
    terms = forms.BooleanField(required=True)

    class Meta:
        model = MyUser
        fields = ('username', 'email', 'first_name', 'last_name', 'city', 'affiliation', 'terms', 'id')
        widgets = {
            'username': forms.TextInput(attrs={'readonly': 'readonly'}),
            'id': forms.HiddenInput(),
        }
        labels = {
            'terms': 'I accept the terms of useTerms and Conditions of Use',
        }
        error_messages = {
            'terms': _('You have to accept the terms of use')
        }

    def __init__(self, *args, **kwargs):
        instance = kwargs.pop('instance', None)
        initial = {}
        request = kwargs.pop('request', None)
        if request is not None and request.META is not None:
            try:
                i = request.META['OIDC_CLAIM_displayName'].index(" ")
                first_name = instance.first_name
                last_name = instance.last_name
                email = instance.email
                if first_name is "":
                    first_name = request.META['OIDC_CLAIM_displayName'][i + 1:].title()
                if last_name is "":
                    last_name = request.META['OIDC_CLAIM_displayName'][:i].title()
                if email is "":
                    email = request.META['OIDC_CLAIM_email']
                initial = {
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                }
                initial_parent = kwargs.pop('initial', None)
                if isinstance(initial_parent, dict):
                    initial.update(initial_parent)
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, file_name, exc_tb.tb_lineno)  # if node is not None:

        super(RegisterUserFromOIDC, self).__init__(initial=initial, instance=instance, *args, **kwargs)
