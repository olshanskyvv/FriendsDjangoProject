from django.urls import path

from .views import *

urlpatterns = [
    path('users', UserAPIView.as_view()),
]
