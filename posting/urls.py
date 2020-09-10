from django.urls import path

from .views import (
    CommentView,
    CommentsView
)

urlpatterns = [
    path('/comment', CommentsView.as_view()),
    path('/comment/<int:comment_id>', CommentView.as_view()),
]
