from django import forms
from .models import Item, Loan
from django.contrib.auth.forms import AuthenticationForm


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
