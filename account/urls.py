from django.urls import path

from .views import (
    SignUpView,
    SignInView,
    KakaoLoginView,
    GoogleLoginView,
    DogView,
)

urlpatterns = [
    path('', SignUpView.as_view()),
    path('/login', SignInView.as_view()),
    path('/kakao', KakaoLoginView.as_view()),
    path('/google', GoogleLoginView.as_view()),
    path('/dogs', DogView.as_view()),
]
