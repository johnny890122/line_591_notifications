from django.contrib import admin
from django.urls import path
from . import views
from line_591_notifications.api import auth, notify

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.homepage),
    path("auth/", auth),
    path('notify/', notify),
]
