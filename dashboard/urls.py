from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboardPollsView, name="dashboard"),
    path('polls/', views.dashboardPollsView, name="dashboardPolls"),
    path('account/', views.dashboardAccountsView, name="dashboardAccount"),
    path('account/changeMail', views.changeMailView, name="changeMail"),
    path('account/changePassword', views.changePasswordView, name="changePassword"),
]