from django.urls import path
from . import views

urlpatterns = [
    path('sendVote/<int:id>', views.sendVoteView, name="sendVote"),
    path('viewPoll/<int:id>', views.viewPollView, name="viewPoll"),
]