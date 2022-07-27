from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views.generic.edit import FormView
from django.contrib.auth import logout

from accounts.models import ExtendedUser
from .forms import LoginForm, RegisterForm
from django.contrib.auth.models import User

class SignInView(FormView):
    template_name = 'signIn.html'
    form_class = LoginForm
    success_url = '/'

    def form_valid(self, form):
        user = authenticate(self.request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        login(self.request, user)

        return redirect('/')

class SignUpView(FormView):
    template_name = 'signUp.html'
    form_class = RegisterForm
    success_url = '/'            

    def form_valid(self, form):
        user = User(username=form.cleaned_data['username'], email=form.cleaned_data['email'], password=form.cleaned_data['password'])
        user.save()
        extendedUser = ExtendedUser(user=user, email_verified=False)
        extendedUser.save()

        login(self.request, user)

        return redirect('/')

def signOutView(request):
    logout(request)
    
    return redirect('/')