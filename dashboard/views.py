import math
import re
from django import views
from django.forms import ValidationError
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from accounts.forms import ChangeEmailForm, ChangePasswordForm
from django.views.generic import ListView

from dashboard.fields import PollOption

from polls.models import PollModel
from .forms import CreatePollForm

def getDefaultChangeEmailForm(request):
    return ChangeEmailForm(initial={'email': request.user.email})

class DashboardPollsView(ListView):
    paginate_by = 4
    template_name = "dashboardPolls.html"

    def get_queryset(self):
        polls = list(PollModel.objects.filter(createdBy=self.request.user))

        totalItems = 0
        pollsRows = []
        for rowIndex in range(math.ceil(len(polls) / 4)):
            pollsOfRow = []
            for columnIndex in range(min(4, len(polls) - totalItems)):
                poll = polls[(rowIndex * 4) + columnIndex]
                pollsOfRow.append(poll)

                totalItems += 1
            pollsRows.append(pollsOfRow)
        
        return pollsRows

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
                messages.error("Your current password is incorrect.")
    
    return render(request, "dashboardAccount.html", context={'changeEmailForm': getDefaultChangeEmailForm(request), 'changePasswordForm': form})

@login_required
def createPollView(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        isMultipleSelectionsAllowed = request.POST.get("isMultipleSelectionsAllowed", '') == 'on'
        isSelectionChangeable = request.POST.get("isSelectionChangeable", '') == 'on'
        isPublic = request.POST.get("isPublic", '') == 'on'
        
        options = []
        for optionIndex in range(1, 21):
            optionStr = f"option{optionIndex}"
            if not optionStr in request.POST.dict():
                break
            optionValue = request.POST[optionStr].strip()
            if len(optionValue) == 0:
                continue
            options.append(PollOption(optionValue))

        pollModel = PollModel(title=title, description=description, options=options, createdBy=request.user, isMultipleSelectionsAllowed=isMultipleSelectionsAllowed, isSelectionChangeable=isSelectionChangeable, isPublic=isPublic)
        pollModel.save()

        messages.success(request, "Poll created.")
        return redirect("dashboardPolls")
    return render(request, "dashboardCreatePoll.html", context={"form": CreatePollForm()})

@login_required
def editPollView(request, id):
    pollModel = PollModel.objects.get(pk=id)
    if pollModel.createdBy != request.user:
        return redirect("dashboard")

    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        isMultipleSelectionsAllowed = request.POST.get("isMultipleSelectionsAllowed", '') == 'on'
        isSelectionChangeable = request.POST.get("isSelectionChangeable", '') == 'on'
        isPublic = request.POST.get("isPublic", '') == 'on'

        options = []
        optionsAreModified = False
        for optionIndex in range(1, 21):
            optionName = f"option{optionIndex}"
            optionStr = request.POST.get(optionName, None)
            if optionIndex > len(pollModel.options) or pollModel.options[optionIndex - 1].name != optionStr:
                optionsAreModified = True
            if not optionStr:
                break
            options.append(PollOption(optionStr))
        optionsAreModified = optionsAreModified or len(options) != len(pollModel.options)

        pollModel.title = title
        pollModel.description = description
        if optionsAreModified:
            pollModel.options = options
        pollModel.isMultipleSelectionsAllowed = isMultipleSelectionsAllowed
        pollModel.isSelectionChangeable = isSelectionChangeable
        pollModel.isPublic = isPublic
        pollModel.save()

        messages.success(request, "Poll saved.")
        return redirect("dashboardPolls")
    return render(request, "dashboardEditPoll.html", context={"form": CreatePollForm(instance=pollModel), "formOptions": [option.name for option in pollModel.options], "id": id})

@login_required
def removePollView(request, id):
    pollModel = PollModel.objects.get(pk=id)
    if pollModel.createdBy != request.user:
        return redirect("dashboard")
    
    pollModel.delete()

    return redirect("dashboard")