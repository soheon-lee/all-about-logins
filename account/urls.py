from django.urls import path

from .views import (
    SignUpView,
    SignInView,
    KakaoLoginView,
    GoogleLoginView
)

urlpatterns = [
    path('/signup', SignUpView.as_view()),
    path('/signin', SignInView.as_view()),
    path('/kakao', KakaoLoginView.as_view()),
    path('/google', GoogleLoginView.as_view()),
]
