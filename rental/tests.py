from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Item, Loan


class RentalWorkflowTests(TestCase):
    def setUp(self):
        self.student = User.objects.create_user(username="student", password="pass")
        self.admin = User.objects.create_user(username="admin", password="pass", is_staff=True)
        self.item = Item.objects.create(name="MacBook Air", category="PC", status="available")

    def test_student_can_borrow_available_item(self):
        self.client.force_login(self.student)

        response = self.client.post(
            reverse("rental:borrow_item", args=[self.item.id]),
            {
                "student_name": "山田 太郎",
                "student_number": "S001",
                "purpose": "授業利用",
                "return_due_date": timezone.localdate() + timedelta(days=7),
            },
        )

        self.assertRedirects(response, reverse("rental:borrow_complete"))
        self.item.refresh_from_db()
        self.assertEqual(self.item.status, "borrowed")
        self.assertEqual(Loan.objects.get(item=self.item).status, "borrowed")

    def test_non_staff_user_cannot_open_admin_loan_list(self):
        self.client.force_login(self.student)

        response = self.client.get(reverse("rental:loan_list"))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response["Location"])

    def test_admin_can_return_borrowed_item(self):
        loan = Loan.objects.create(
            item=self.item,
            student_name="山田 太郎",
            student_number="S001",
            purpose="授業利用",
            return_due_date=timezone.localdate() + timedelta(days=7),
            status="borrowed",
        )
        self.item.status = "borrowed"
        self.item.save()
        self.client.force_login(self.admin)

        response = self.client.post(reverse("rental:return_item", args=[loan.id]))

        self.assertRedirects(response, reverse("rental:loan_list"))
        loan.refresh_from_db()
        self.item.refresh_from_db()
        self.assertEqual(loan.status, "returned")
        self.assertEqual(self.item.status, "available")

    def test_admin_page_redirects_to_app_login_when_not_logged_in(self):
        response = self.client.get(reverse("admin:index"))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response["Location"])
        self.assertIn("next=/admin/", response["Location"])

    def test_student_cannot_open_admin_page(self):
        self.client.force_login(self.student)

        response = self.client.get(reverse("admin:index"))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response["Location"])

    def test_staff_user_can_open_admin_page(self):
        self.client.force_login(self.admin)

        response = self.client.get(reverse("admin:index"))

        self.assertEqual(response.status_code, 200)
