from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    student_number = models.CharField("学籍番号", max_length=20, blank=True)

    class Meta:
        verbose_name = "利用者プロフィール"
        verbose_name_plural = "利用者プロフィール"

    def __str__(self):
        return f"{self.user.username} - {self.student_number or '学籍番号未設定'}"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        Profile.objects.get_or_create(user=instance)
from django.db import models
from django.utils import timezone


class Item(models.Model):
    CATEGORY_CHOICES = [
        ("PC", "PC"),
        ("VR", "VRゴーグル"),
        ("Accessory", "周辺機器"),
        ("Other", "その他"),
    ]

    STATUS_CHOICES = [
        ("available", "貸出可能"),
        ("borrowed", "貸出中"),
        ("broken", "故障中"),
    ]

    name = models.CharField("備品名", max_length=100)
    category = models.CharField("種類", max_length=20, choices=CATEGORY_CHOICES)
    status = models.CharField("状態", max_length=20, choices=STATUS_CHOICES, default="available")
    note = models.TextField("備考", blank=True)
    created_at = models.DateTimeField("登録日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)

    class Meta:
        verbose_name = "備品"
        verbose_name_plural = "備品"

    def __str__(self):
        return self.name


class Loan(models.Model):
    LOAN_STATUS_CHOICES = [
        ("borrowed", "貸出中"),
        ("returned", "返却済み"),
    ]

    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name="備品")
    student_name = models.CharField("学生名", max_length=50)
    student_number = models.CharField("学籍番号", max_length=20)
    purpose = models.TextField("使用目的")
    borrow_date = models.DateField("貸出日", default=timezone.localdate)
    return_due_date = models.DateField("返却予定日")
    return_date = models.DateField("返却日", null=True, blank=True)
    status = models.CharField("貸出状態", max_length=20, choices=LOAN_STATUS_CHOICES, default="borrowed")
    created_at = models.DateTimeField("申請日時", auto_now_add=True)

    class Meta:
        verbose_name = "貸出"
        verbose_name_plural = "貸出"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.item.name} - {self.student_name}"

    def is_overdue(self):
        return self.status == "borrowed" and self.return_due_date < timezone.localdate()
