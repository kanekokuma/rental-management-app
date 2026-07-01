import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "環境変数から管理者ユーザーを作成または更新します"

    def handle(self, *args, **options):
        username = os.environ.get("ADMIN_USERNAME")
        password = os.environ.get("ADMIN_PASSWORD")
        email = os.environ.get("ADMIN_EMAIL", "")

        if not username or not password:
            self.stdout.write("ADMIN_USERNAME / ADMIN_PASSWORD が未設定のため、管理者作成をスキップしました。")
            return

        User = get_user_model()
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "email": email,
                "is_staff": True,
                "is_superuser": True,
            },
        )

        user.email = email
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()

        action = "作成" if created else "更新"
        self.stdout.write(self.style.SUCCESS(f"管理者ユーザー {username} を{action}しました。"))
