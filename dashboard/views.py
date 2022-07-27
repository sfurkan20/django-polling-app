from django.forms import ValidationError
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.forms import ChangeEmailForm, ChangePasswordForm

def getDefaultChangeEmailForm(request):
    return ChangeEmailForm(initial={'email': request.user.email})

@login_required
def dashboardPollsView(request):
    return render(request, "dashboardPolls.html")

@login_required
def dashboardAccountsView(request):
    return render(request, "dashboardAccount.html", context={'changeEmailForm': getDefaultChangeEmailForm(request), 'changePasswordForm': ChangePasswordForm()})

@login_required
def changeMailView(request):
    if request.method == "POST":
        request.user.email = request.POST["email"]
        request.user.save()
        messages.success(request, "E-mail is successfully changed.", extra_tags="SUCCESS")
        
    return redirect("/dashboard/account")

@login_required
def changePasswordView(request):
    if request.method == "POST":
        user = request.user
        form = ChangePasswordForm(request.POST)

        if form.is_valid():
            if user.check_password(form.cleaned_data["currentPassword"]):
                user.set_password(form.cleaned_data["password"])
                user.save()
            else:
                form.add_error(field="", error=ValidationError("Your current password is incorrect."))
    
    return render(request, "dashboardAccount.html", context={'changeEmailForm': getDefaultChangeEmailForm(request), 'changePasswordForm': form})