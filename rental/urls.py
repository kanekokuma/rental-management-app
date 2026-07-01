from django.urls import path
from . import views
from rental.forms import SecureLoginForm

app_name = "rental"

urlpatterns = [
    path("", views.index, name="index"),
    path("items/", views.item_list, name="item_list"),
    path("items/<int:item_id>/", views.item_detail, name="item_detail"),
    path("items/create/", views.item_create, name="item_create"),
    path("items/<int:item_id>/edit/", views.item_edit, name="item_edit"),
    path("items/<int:item_id>/delete/", views.item_delete, name="item_delete"),
    path("items/<int:item_id>/borrow/", views.borrow_item, name="borrow_item"),
    path("borrow/complete/", views.borrow_complete, name="borrow_complete"),
    path("loans/", views.loan_list, name="loan_list"),
    path("loans/<int:loan_id>/return/", views.return_item, name="return_item"),
    path("history/", views.loan_history, name="loan_history"),
    path(
    "accounts/login/",
    auth_views.LoginView.as_view(template_name="registration/login.html", authentication_form=SecureLoginForm),
    name="login",
    ),
]
