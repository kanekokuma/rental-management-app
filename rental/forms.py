from django import forms
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
