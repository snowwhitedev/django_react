from django.urls import path

from .views import index, policy, repetition, users
# , TodoDetailView

urlpatterns = [
    path('', index),
    path('policy', policy),
    path('repetition', repetition),
    path('users', users)
    # path('delete/<int:pk>', TodoDetailView.as_view()),
]