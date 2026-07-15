from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from rental.views import AppLoginView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("rental.urls")),
    path(
        "accounts/login/",
        AppLoginView.as_view(),
        name="login",
    ),
    path(
        "accounts/logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),
]
