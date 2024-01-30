from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission

@receiver(post_save, sender=User)
def assign_staff_permissions(sender, instance, created, **kwargs):
    if instance.is_staff:
        # List of permissions to be assigned
        permissions = [
            'delete_credential', 
            'delete_network', 
            'delete_server', 
            'delete_servercredential', 
            'delete_serverservice', 
            'delete_service', 
            'delete_servicecredential'
        ]

        for perm in permissions:
            permission = Permission.objects.get(codename=perm, content_type__app_label='hmlsvcrapp')
            instance.user_permissions.add(permission)
