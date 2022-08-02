from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db.models import Q
from polling_site.fields import PasswordField
from django.contrib.auth.password_validation import CommonPasswordValidator

# I used plain Form class instead of ModelForm class, since doing so would be a great way to understand the stuff going in the back.
class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'name': 'username', 'id':'username', 'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'name': 'password', 'id':'password', 'class': 'form-control'}))

    class Meta:
	    model = User
	    fields = ("username", "password")

    def clean(self):
        username = self.cleaned_data["username"]
        password = self.cleaned_data["password"]

        return self.cleaned_data

class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'name': 'username', 'id':'username', 'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'name': 'email', 'id':'email', 'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'name': 'password', 'id':'password', 'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'name': 'password2', 'id':'password2', 'class': 'form-control'}))

    class Meta:
	    model = User
	    fields = ("username", "email", "password", "password2")

    def clean(self):
        username = self.cleaned_data["username"]
        email = self.cleaned_data["email"]
        password = self.cleaned_data["password"]
        password2 = self.cleaned_data["password2"]

        if User.objects.filter(Q(username=username) | Q(email=email)).exists():
            raise forms.ValidationError("Given username or email already exists in the system.")
        
        if password != password2:
            raise forms.ValidationError("Passwords do not match.")

        return self.cleaned_data

class ChangeEmailForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'name': 'email', 'id':'email', 'class': 'form-control'}))

class ChangePasswordForm(forms.Form):
    currentPassword = forms.CharField(widget=forms.PasswordInput(attrs={'name': 'currentPassword', 'id':'currentPassword', 'class': 'form-control', 'placeholder': 'Current password'}), validators=[CommonPasswordValidator().validate])
    password = forms.CharField(widget=forms.PasswordInput(attrs={'name': 'password', 'id':'password', 'class': 'form-control', 'placeholder': 'New password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'name': 'password2', 'id':'password2', 'class': 'form-control', 'placeholder': 'Retype new password'}))
    
    def clean(self):
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']

        if password != password2:
            raise forms.ValidationError("Passwords do not match.")

        return self.cleaned_data