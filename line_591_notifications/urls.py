from django.contrib import admin
from django.urls import path
from . import views
import line_591_notifications.api as api
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.homepage),
    path("auth/", api.auth),
    path('notify/', api.notify),
    path('login/', api.login)
]
