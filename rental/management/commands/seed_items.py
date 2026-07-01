from django.core.management.base import BaseCommand
from rental.models import Item

class Command(BaseCommand):
    help = "サンプル備品データを登録します"

    def handle(self, *args, **options):
        data = [
            {"name": "MacBook Air", "category": "PC", "status": "available", "note": "授業・開発用"},
            {"name": "WindowsノートPC", "category": "PC", "status": "available", "note": "Office利用可能"},
            {"name": "Meta Quest 3", "category": "VR", "status": "available", "note": "VR開発・検証用"},
            {"name": "Meta Quest 2", "category": "VR", "status": "available", "note": "予備機"},
            {"name": "HDMIケーブル", "category": "Accessory", "status": "available", "note": "発表用"},
        ]

        for item in data:
            Item.objects.get_or_create(name=item["name"], defaults=item)

        self.stdout.write(self.style.SUCCESS("サンプル備品データを登録しました。"))
