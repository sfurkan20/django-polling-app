from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from dashboard.fields import PollOptionField

class PollModel(models.Model):
    title = models.CharField(max_length=50, blank=False)
    description = models.CharField(max_length=1000, default="")
    options = ArrayField(PollOptionField(max_length=150))
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    isMultipleSelectionsAllowed = models.BooleanField(default=True)
    isSelectionChangeable = models.BooleanField(default=True)
    isPublic = models.BooleanField(default=True)

    creationDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(auto_now=True)

class IPVoteRegistry(models.Model):
    ip = models.GenericIPAddressField()
    poll = models.ForeignKey(PollModel, on_delete=models.CASCADE)
    voteOptionStr = models.CharField(max_length=150, default="")

    actionDate = models.DateTimeField(auto_now_add=True)

class UserVoteRegistry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(PollModel, on_delete=models.CASCADE)
    voteOptionStr = models.CharField(max_length=150, default="")

    actionDate = models.DateTimeField(auto_now_add=True)