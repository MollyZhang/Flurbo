from django import forms
from django.contrib.auth.models import User
from bootstrap_toolkit.widgets import BootstrapDateInput, BootstrapTextInput, BootstrapUneditableInput

class LoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        label=u"Username",
        error_messages={'required': 'Please enter username!'},
        widget=forms.TextInput(
            attrs={
                'placeholder':u"Username",
            }
        ),
    )
    password = forms.CharField(
        required=True,
        label=u"Password",
        error_messages={'required': u'Please Enter password'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder':u"password",
            }
        ),
    )
    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u"You must enter username and password")
        else:
            cleaned_data = super(LoginForm, self).clean()
