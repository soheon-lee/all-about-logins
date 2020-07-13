from .views import (
    SignUpView,
    SignInView,
)

from django.urls import path

urlpatterns = [
   path('', SignUpView.as_view()), 
   path('/login', SignInView.as_view()), 
]
