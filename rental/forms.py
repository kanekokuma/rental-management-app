from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Item, Loan


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ["name", "category", "status", "note"]
        widgets = {
            "note": forms.Textarea(attrs={"rows": 3}),
        }


class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ["purpose", "return_due_date"]
        widgets = {
            "return_due_date": forms.DateInput(attrs={"type": "date"}),
            "purpose": forms.Textarea(attrs={"rows": 3}),
        }


class SecureLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="ユーザー名",
        widget=forms.TextInput(attrs={"autocomplete": "username", "autocapitalize": "none"}),
    )
    password = forms.CharField(
        label="パスワード",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )


class StudentUserCreationForm(UserCreationForm):
    first_name = forms.CharField(label="姓", required=False)
    last_name = forms.CharField(label="名", required=False)
    student_number = forms.CharField(label="学籍番号", max_length=20, required=False)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "student_number")

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            profile, _ = user.profile.__class__.objects.get_or_create(user=user)
            profile.student_number = self.cleaned_data.get("student_number", "")
            profile.save()
        return user


class StudentUserChangeForm(UserChangeForm):
    student_number = forms.CharField(label="学籍番号", max_length=20, required=False)

    class Meta:
        model = User
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            profile = getattr(self.instance, "profile", None)
            self.fields["student_number"].initial = getattr(profile, "student_number", "")

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            profile, _ = user.profile.__class__.objects.get_or_create(user=user)
            profile.student_number = self.cleaned_data.get("student_number", "")
            profile.save()
        return user
