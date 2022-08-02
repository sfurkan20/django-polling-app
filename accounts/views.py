from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views.generic import TemplateView, FormView
from django.contrib.auth import logout

from accounts.models import ExtendedUser
from .forms import LoginForm, RegisterForm
from django.contrib.auth.models import User

def signInView(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data["username"], password=form.cleaned_data["password"])
            if not user or not user.is_active:
                messages.error(request, "Check your username and password.")
            else:
                login(request, user)
                return redirect("/")
    return render(request, "signIn.html", context={"form": form})

class SignUpView(FormView):
    template_name = 'signUp.html'
    form_class = RegisterForm
    success_url = '/'            

    def form_valid(self, form):
        user = User(username=form.cleaned_data['username'], email=form.cleaned_data['email'])
        user.set_password(form.cleaned_data['password'])
        user.save()
        extendedUser = ExtendedUser(user=user, email_verified=False)
        extendedUser.save()

        login(self.request, user)

        return redirect('/')

def signOutView(request):
    logout(request)
    
    return redirect('/')