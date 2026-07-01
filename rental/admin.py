from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .forms import StudentUserChangeForm, StudentUserCreationForm
from .models import Item, Loan, Profile


admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    form = StudentUserChangeForm
    add_form = StudentUserCreationForm

    list_display = ("username", "get_full_name", "get_student_number", "is_staff", "is_active")
    search_fields = ("username", "first_name", "last_name", "profile__student_number")

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("本人情報", {"fields": ("first_name", "last_name", "student_number")}),
        ("権限", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("重要な日付", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "first_name", "last_name", "student_number", "password1", "password2"),
        }),
    )

    @admin.display(description="学籍番号")
    def get_student_number(self, obj):
        return getattr(getattr(obj, "profile", None), "student_number", "")


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "status", "updated_at")
    list_filter = ("category", "status")
    search_fields = ("name", "note")


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ("id", "item", "student_name", "student_number", "status", "borrow_date", "return_due_date", "return_date")
    list_filter = ("status", "borrow_date", "return_due_date")
    search_fields = ("student_name", "student_number", "purpose", "item__name")


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "student_number")
    search_fields = ("user__username", "user__first_name", "user__last_name", "student_number")
