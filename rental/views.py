from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import ItemForm, LoanForm
from .models import Item, Loan


def is_admin(user):
    return user.is_staff


def get_user_identity(user):
    name = user.get_full_name() or user.username
    profile = getattr(user, "profile", None)
    student_number = getattr(profile, "student_number", "")
    return name, student_number


def index(request):
    today = timezone.localdate()
    dashboard = {
        "total_items": Item.objects.count(),
        "available_items": Item.objects.filter(status="available").count(),
        "pending_items": Item.objects.filter(status="pending").count(),
        "borrowed_items": Item.objects.filter(status="borrowed").count(),
        "broken_items": Item.objects.filter(status="broken").count(),
        "pending_loans": Loan.objects.filter(status="pending").count(),
        "borrowed_loans": Loan.objects.filter(status="borrowed").count(),
        "overdue_loans": Loan.objects.filter(status="borrowed", return_due_date__lt=today).count(),
        "returned_loans": Loan.objects.filter(status="returned").count(),
    }
    return render(request, "rental/index.html", {"dashboard": dashboard})


@login_required
def item_list(request):
    category = request.GET.get("category")
    status = request.GET.get("status")

    items = Item.objects.all().order_by("id")

    if category:
        items = items.filter(category=category)
    if status:
        items = items.filter(status=status)

    context = {
        "items": items,
        "category": category,
        "status": status,
        "category_choices": Item.CATEGORY_CHOICES,
        "status_choices": Item.STATUS_CHOICES,
    }
    return render(request, "rental/item_list.html", context)


@login_required
def item_detail(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    active_loan = Loan.objects.filter(item=item, status__in=["pending", "borrowed"]).first()
    return render(request, "rental/item_detail.html", {"item": item, "active_loan": active_loan})


@user_passes_test(is_admin)
def item_create(request):
    if request.method == "POST":
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "備品を登録しました。")
            return redirect("rental:item_list")
    else:
        form = ItemForm()

    return render(request, "rental/item_form.html", {"form": form, "title": "備品追加"})


@user_passes_test(is_admin)
def item_edit(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    if request.method == "POST":
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "備品情報を更新しました。")
            return redirect("rental:item_detail", item_id=item.id)
    else:
        form = ItemForm(instance=item)

    return render(request, "rental/item_form.html", {"form": form, "title": "備品編集"})


@user_passes_test(is_admin)
def item_delete(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    if request.method == "POST":
        item.delete()
        messages.success(request, "備品を削除しました。")
        return redirect("rental:item_list")

    return render(request, "rental/item_confirm_delete.html", {"item": item})


@login_required
def borrow_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    student_name, student_number = get_user_identity(request.user)

    if item.status != "available":
        messages.error(request, "この備品は現在貸出できません。")
        return redirect("rental:item_detail", item_id=item.id)

    if not student_number:
        messages.error(request, "貸出申請には学籍番号の登録が必要です。管理者にユーザー情報の登録を依頼してください。")
        return redirect("rental:item_detail", item_id=item.id)

    if request.method == "POST":
        form = LoanForm(request.POST)
        if form.is_valid():
            loan = form.save(commit=False)
            loan.item = item
            loan.student_name = student_name
            loan.student_number = student_number
            loan.status = "pending"
            loan.borrow_date = timezone.localdate()
            loan.save()

            item.status = "pending"
            item.save()

            messages.success(request, "貸出申請を送信しました。管理者の受理後に貸出中になります。")
            return redirect("rental:borrow_complete")
    else:
        form = LoanForm()

    context = {
        "form": form,
        "item": item,
        "student_name": student_name,
        "student_number": student_number,
    }
    return render(request, "rental/borrow_form.html", context)


@login_required
def borrow_complete(request):
    return render(request, "rental/borrow_complete.html")


@user_passes_test(is_admin)
def application_list(request):
    loans = Loan.objects.filter(status="pending").select_related("item")
    return render(request, "rental/application_list.html", {"loans": loans})


@user_passes_test(is_admin)
def approve_loan(request, loan_id):
    loan = get_object_or_404(Loan, id=loan_id, status="pending")

    if request.method == "POST":
        if loan.item.status != "pending":
            messages.error(request, "この備品は現在受理できる状態ではありません。")
            return redirect("rental:application_list")

        loan.status = "borrowed"
        loan.borrow_date = timezone.localdate()
        loan.save()

        loan.item.status = "borrowed"
        loan.item.save()

        messages.success(request, "貸出申請を受理しました。")
        return redirect("rental:loan_list")

    return render(request, "rental/approve_confirm.html", {"loan": loan})


@user_passes_test(is_admin)
def loan_list(request):
    loans = Loan.objects.filter(status="borrowed").select_related("item")
    return render(request, "rental/loan_list.html", {"loans": loans})


@user_passes_test(is_admin)
def return_item(request, loan_id):
    loan = get_object_or_404(Loan, id=loan_id, status="borrowed")

    if request.method == "POST":
        loan.status = "returned"
        loan.return_date = timezone.localdate()
        loan.save()

        loan.item.status = "available"
        loan.item.save()

        messages.success(request, "返却処理が完了しました。")
        return redirect("rental:loan_list")

    return render(request, "rental/return_confirm.html", {"loan": loan})


@user_passes_test(is_admin)
def loan_history(request):
    loans = Loan.objects.all().select_related("item")
    return render(request, "rental/loan_history.html", {"loans": loans})
