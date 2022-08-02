import re
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import PollModel, IPVoteRegistry, UserVoteRegistry
from ipware import get_client_ip


def viewPollView(request, id):
    pollModel = PollModel.objects.get(pk=id)
    if not pollModel.isPublic and pollModel.createdBy != request.user:
        return None
    
    options = []  # tuple (optionStr, voteCount, percentage)
    totalVotes = 0
    for option in pollModel.options:
        totalVotes += option.voteCount
    for option in pollModel.options:
        percentage = 0
        if totalVotes != 0:
            percentage = 100 * (option.voteCount / totalVotes)
        options.append((option.name, option.voteCount, percentage))
    pollModel.options = options


    canVote = (IPVoteRegistry.objects.filter(ip=get_client_ip(request)[0], poll=pollModel).count() == 0)
    if request.user.is_authenticated:
        canVote = canVote and (UserVoteRegistry.objects.filter(user=request.user, poll=pollModel).count() == 0)
    canVote = canVote or pollModel.isSelectionChangeable

    return render(request, "viewPoll.html", context={"poll": pollModel, "pollId": id, "canVote": canVote})

def sendVoteView(request, id):
    pollModel = PollModel.objects.get(pk=id)
    if request.method == "POST":
        selectionStrs = []
        multipleSelections = "optionRadio" in request.POST.dict()
        if multipleSelections:
            optionIndex = int(request.POST["optionRadio"]) - 1
            pollModel.options[optionIndex].voteCount += 1
            selectionStrs.append(pollModel.options[optionIndex].name)
        else:
            for key in request.POST:
                numberMatch = re.findall("(?<=checkbox)[1-9]+", key)
                if len(numberMatch) == 1:
                    optionIndex = int(numberMatch[0]) - 1
                    pollModel.options[optionIndex].voteCount += 1
                    selectionStrs.append(pollModel.options[optionIndex].name)

        prevVoteIPQuerySet = IPVoteRegistry.objects.filter(ip=get_client_ip(request)[0], poll=pollModel)
        prevVoteUserQuerySet = UserVoteRegistry.objects.filter(user=request.user, poll=pollModel)

        prevVote = list(prevVoteIPQuerySet)
        if len(prevVote) == 0 and request.user.is_authenticated:
            prevVote = list(prevVoteUserQuerySet)
        if len(prevVote) > 0:
            for previousVote in prevVote:
                for idx, option in enumerate(pollModel.options):
                    if option.name == previousVote.voteOptionStr:
                        pollModel.options[idx].voteCount = max(pollModel.options[idx].voteCount - 1, 0)
        pollModel.save()

        prevVoteIPQuerySet.delete()
        prevVoteUserQuerySet.delete()

        for selection in selectionStrs:
            ipRegistry = IPVoteRegistry(ip=get_client_ip(request)[0], poll=pollModel, voteOptionStr=selection)
            ipRegistry.save()

            if request.user.is_authenticated:
                userRegistry = UserVoteRegistry(user=request.user, poll=pollModel, voteOptionStr=selection)
                userRegistry.save()

        messages.success(request, "Your vote has been successfully submitted.")
        return redirect("viewPoll", id)