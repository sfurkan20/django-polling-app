from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    path('', login_required(views.DashboardPollsView.as_view()), name="dashboard"),
    path('polls/', login_required(views.DashboardPollsView.as_view()), name="dashboardPolls"),
    path('account/', views.dashboardAccountsView, name="dashboardAccount"),
    path('account/changeMail', views.changeMailView, name="changeMail"),
    path('account/changePassword', views.changePasswordView, name="changePassword"),
    path('polls/createPoll', views.createPollView, name="createPoll"),
    path('polls/editPoll/<int:id>', views.editPollView, name="editPoll"),
    path('polls/removePoll/<int:id>', views.removePollView, name="removePoll"),
]