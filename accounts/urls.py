from django.urls import path

from . import views

urlpatterns = [
    path('signIn/', views.SignInView.as_view(), name='signIn'),
    path('signUp/', views.SignUpView.as_view(), name='signUp'),
    path('signOut/', views.signOutView, name='signOut'),
]