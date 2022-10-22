from django.contrib import admin
from django.urls import path
from .views import (RegisterView, LoginAPIView, profile_detail_api_view)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('<str:username>/', profile_detail_api_view, name='profile')
]
