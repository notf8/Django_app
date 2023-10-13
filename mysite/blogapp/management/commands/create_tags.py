from django.core.management import BaseCommand
from blogapp.models import Tag


class Command(BaseCommand):
    """
    Creates new tag's
    """

    def handle(self, *args, **options):
        self.stdout.write("Create tag")

        tags_names = [
            "Fan",
            "Speed",
            "Money",
            "Dogs",
            "Cats",
            "Ocean",
            "Mountains",
            "Woods",
            "Flavors",
            "Hills",
            "Journey",
            "Exploration",
            "City",
            "Natural",
        ]

        for tag_name in tags_names:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            self.stdout.write(f"Create tag: {tag.name}")

        self.stdout.write(self.style.SUCCESS("Tag's created"))
