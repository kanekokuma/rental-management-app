# Generated for the cloud-ready equipment rental app.

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Item",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, verbose_name="備品名")),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("PC", "PC"),
                            ("VR", "VRゴーグル"),
                            ("Accessory", "周辺機器"),
                            ("Other", "その他"),
                        ],
                        max_length=20,
                        verbose_name="種類",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("available", "貸出可能"),
                            ("borrowed", "貸出中"),
                            ("broken", "故障中"),
                        ],
                        default="available",
                        max_length=20,
                        verbose_name="状態",
                    ),
                ),
                ("note", models.TextField(blank=True, verbose_name="備考")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="登録日時")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="更新日時")),
            ],
            options={
                "verbose_name": "備品",
                "verbose_name_plural": "備品",
            },
        ),
        migrations.CreateModel(
            name="Loan",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("student_name", models.CharField(max_length=50, verbose_name="学生名")),
                ("student_number", models.CharField(max_length=20, verbose_name="学籍番号")),
                ("purpose", models.TextField(verbose_name="使用目的")),
                ("borrow_date", models.DateField(default=django.utils.timezone.localdate, verbose_name="貸出日")),
                ("return_due_date", models.DateField(verbose_name="返却予定日")),
                ("return_date", models.DateField(blank=True, null=True, verbose_name="返却日")),
                (
                    "status",
                    models.CharField(
                        choices=[("borrowed", "貸出中"), ("returned", "返却済み")],
                        default="borrowed",
                        max_length=20,
                        verbose_name="貸出状態",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="申請日時")),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="rental.item",
                        verbose_name="備品",
                    ),
                ),
            ],
            options={
                "verbose_name": "貸出",
                "verbose_name_plural": "貸出",
                "ordering": ["-created_at"],
            },
        ),
    ]
