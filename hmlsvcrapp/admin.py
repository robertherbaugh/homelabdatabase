from django.contrib import admin
from .models import Server, Service, Network, Credential
from django.contrib.admin import AdminSite

admin.site.register(Server)
admin.site.register(Service)
admin.site.register(Network)
admin.site.register(Credential)

class MyAdminSite(AdminSite):
    def has_permission(self, request):
        return request.user.is_active and request.user.is_superuser

admin_site = MyAdminSite(name='myadmin')