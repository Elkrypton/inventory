from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from .views import *


urlpatterns = [
    path('ask/', chatbot_ask, name="chatbot-ask"),
]