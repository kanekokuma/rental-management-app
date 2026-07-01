from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import ItemForm, LoanForm
from .models import Item, Loan


def is_admin(user):
    return user.is_staff


def index(request):
    return render(request, "rental/index.html")


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
    active_loan = Loan.objects.filter(item=item, status="borrowed").first()
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

    if item.status != "available":
        messages.error(request, "この備品は現在貸出できません。")
        return redirect("rental:item_detail", item_id=item.id)

    if request.method == "POST":
        form = LoanForm(request.POST)
        if form.is_valid():
            loan = form.save(commit=False)
            loan.item = item
            loan.status = "borrowed"
            loan.borrow_date = timezone.localdate()
            loan.save()

            item.status = "borrowed"
            item.save()

            messages.success(request, "貸出申請が完了しました。")
            return redirect("rental:borrow_complete")
    else:
        initial = {}
        if request.user.is_authenticated:
            initial["student_name"] = request.user.get_full_name() or request.user.username
        form = LoanForm(initial=initial)

    return render(request, "rental/borrow_form.html", {"form": form, "item": item})


@login_required
def borrow_complete(request):
    return render(request, "rental/borrow_complete.html")


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
