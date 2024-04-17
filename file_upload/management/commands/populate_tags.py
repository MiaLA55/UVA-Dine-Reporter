from django.core.management.base import BaseCommand
from file_upload.models import Tag

class Command(BaseCommand):
    help = 'Populate tags in the database'

    def handle(self, *args, **options):
        tags_data = [
            {'name': 'Allergens, Other Special Dietary Needs'},
            {'name': 'Cleanliness'},
            {'name': 'Quality of Ingredients'},
            {'name': 'Service'},
            {'name': 'Spoiled Food'},
            {'name': 'Taste'},
            {'name': 'Temperature'},
            {'name': 'Undercooked Food'},
            {'name': 'Wait Time'},
        ]

        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(**tag_data)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Tag "{tag.name}" created'))
            else:
                self.stdout.write(self.style.WARNING(f'Tag "{tag.name}" already exists'))
