from pydoc import locate
from django import forms
from polling_site.settings import AUTH_PASSWORD_VALIDATORS

class PasswordField(forms.CharField):
    min_length = 5
    max_length = 20
    widget=forms.PasswordInput
    validators=[locate(validatorDict['NAME']).validate for validatorDict in AUTH_PASSWORD_VALIDATORS]