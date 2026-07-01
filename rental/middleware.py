from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse


class AdminAccessFromAppLoginMiddleware:
    """Require a staff account logged in through the app before opening /admin/."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        admin_path = reverse("admin:index")
        if request.path.startswith(admin_path) and not request.path.startswith(f"{settings.STATIC_URL}admin/"):
            if not request.user.is_authenticated:
                return redirect(f"{reverse(settings.LOGIN_URL)}?next={request.get_full_path()}")

            if not request.user.is_staff:
                messages.error(request, "管理者アカウントでログインしてください。")
                return redirect(f"{reverse(settings.LOGIN_URL)}?next={request.get_full_path()}")

        return self.get_response(request)
