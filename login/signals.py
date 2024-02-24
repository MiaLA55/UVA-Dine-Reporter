from django.contrib.auth.models import Group
from django.db.models.signals import post_migrate
from django.dispatch import receiver

@receiver(post_migrate)
def create_site_admin_group(sender, **kwargs):
    if kwargs.get('app_config').label == 'login':
        if not Group.objects.filter(name='Site Admin').exists():
            Group.objects.create(name='Site Admin')
