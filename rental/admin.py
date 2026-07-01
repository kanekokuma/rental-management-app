from django.contrib import admin
from .models import Item, Loan

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
