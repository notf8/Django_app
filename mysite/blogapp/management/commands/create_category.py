from django.core.management import BaseCommand
from blogapp.models import Category


class Command(BaseCommand):
    """
    Creates new category's
    """

    def handle(self, *args, **options):
        self.stdout.write("Create category")

        category_names = [
            "Sport",
            "Cars",
            "Vacation",
            "Gadgets",
            "Shopping",
            "Others",
        ]

        for category_name in category_names:
            category, created = Category.objects.get_or_create(name=category_name)
            self.stdout.write(f"Created category: {category.name}")

        self.stdout.write(self.style.SUCCESS("Category's created"))

