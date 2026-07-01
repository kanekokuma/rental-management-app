from django.contrib import admin
from django.contrib.admin.sites import NotRegistered
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .forms import StudentUserChangeForm, StudentUserCreationForm
from .models import Item, Loan, Profile


try:
    admin.site.unregister(User)
except NotRegistered:
    pass


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    form = StudentUserChangeForm
    add_form = StudentUserCreationForm

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("本人情報", {"fields": ("first_name", "last_name", "student_number")}),
        ("権限", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("重要な日付", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "first_name", "last_name", "student_number", "password1", "password2"),
            },
        ),
    )

    list_display = ("username", "get_full_name", "get_student_number", "is_staff", "is_active")
    search_fields = ("username", "first_name", "last_name", "profile__student_number")

    @admin.display(description="学籍番号")
    def get_student_number(self, obj):
        return getattr(getattr(obj, "profile", None), "student_number", "")

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if "student_number" in form.cleaned_data:
            profile, _ = Profile.objects.get_or_create(user=obj)
            profile.student_number = form.cleaned_data["student_number"]
            profile.save()


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
