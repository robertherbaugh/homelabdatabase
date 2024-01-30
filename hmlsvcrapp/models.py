from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from django.db import models

import ipaddress

def generate_subnet_mask_choices():
    choices = []
    for cidr in range(32, -1, -1):  # Starts at 32, ends at 0, steps backwards
        mask = str(ipaddress.IPv4Network(f'0.0.0.0/{cidr}').netmask)
        num_hosts = 2 ** (32 - cidr) - 2  # Usable hosts
        # Handling special cases for /31 and /32 subnets
        if cidr in [31, 32]:
            host_info = 'Self' if cidr == 32 else '1 usable host (point-to-point)'
        else:
            host_info = f'{num_hosts} hosts'
        choices.append((f'/{cidr} - {mask} - {host_info}', f'/{cidr} - {mask} - {host_info}'))
    return choices

class Network(models.Model):
    name = models.CharField(max_length=255)
    vlan_id = models.IntegerField()
    ip_space = models.CharField(max_length=18)
    subnet_mask = models.CharField(max_length=255, choices=generate_subnet_mask_choices())

    def __str__(self):
        return self.name

class Server(models.Model):
    SERVER_TYPES = [
        ('VM', 'Virtual Machine'),
        ('Docker', 'Docker'),
        ('Physical', 'Physical'),
        ('LXC', 'Linux Container'),
        ('Other', 'Other'),
    ]

    OS_CHOICES = [
        ('Debian', 'Debian'),
        ('Ubuntu', 'Ubuntu'),
        ('Windows', 'Windows'),
        ('OtherLinux', 'Other Linux'),
        ('macOS', 'macOS'),
        ('Other', 'Other'),
    ]

    name = models.CharField(max_length=255)
    ip_address = models.CharField(max_length=15)
    location = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    network = models.ForeignKey(Network, on_delete=models.SET_NULL, null=True, related_name='servers')
    type = models.CharField(max_length=50, choices=SERVER_TYPES)
    os = models.CharField(max_length=50, choices=OS_CHOICES)
    #credentials = models.ManyToManyField('Credential', related_name='servers', blank=True)
    cred_name = models.ForeignKey('Credential', on_delete=models.SET_NULL, null=True, blank=True, related_name='servers', to_field='cred_name')

    def __str__(self):
        return self.name

class Service(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Decommissioned', 'Decommissioned'),
    ]

    server = models.ForeignKey(Server, on_delete=models.SET_NULL, related_name='services', null=True)
    network = models.ForeignKey('Network', on_delete=models.SET_NULL, related_name='services', null=True, blank=True)
    name = models.CharField(max_length=255)
    port = models.IntegerField(validators=[MaxValueValidator(65535)])
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    ip = models.CharField(max_length=15)
    wazuh_agent_installed = models.BooleanField(default=False)
    fqdn = models.CharField(max_length=255, null=True, blank=True)
    cloudflare_proxy_configured = models.BooleanField(default=False)
    reverse_proxy_configured = models.BooleanField(default=False)
    ldn = models.CharField(max_length=255, null=True, blank=True)
    dns_configured = models.BooleanField(default=False)
    credentials = models.ManyToManyField('Credential', related_name='services', blank=True)
    https_enabled = models.BooleanField(default=False)
    cred_name = models.ForeignKey('Credential', on_delete=models.SET_NULL, null=True, blank=True, related_name='services_name', to_field='cred_name')

    def __str__(self):
        return self.name

class Credential(models.Model):
    MFA_SOURCES = [
        ('Phone', 'Phone'),
        ('iCloud', 'iCloud Passwords'),
        ('Bitwarden', 'Bitwarden Passwords'),
        ('None', 'Not configured/available'),
    ]

    ACCOUNT_TYPES = [
        ('Root', 'Root'),
        ('User', 'User'),
        ('Admin', 'Admin'),
        ('Other', 'Other'),
    ]

    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)  # Remember to handle encryption securely
    last_updated = models.DateField(null=True, blank=True)
    mfa_enabled = models.BooleanField()
    mfa_source = models.CharField(max_length=50, choices=MFA_SOURCES, blank=True, null=True)
    sso = models.BooleanField()
    account_type = models.CharField(max_length=50, choices=ACCOUNT_TYPES)
    cred_name = models.CharField(max_length=255, null=True, unique=True)
    #content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True)
    #object_id = models.PositiveIntegerField(null=True, blank=True)
    #related_item = GenericForeignKey('content_type', 'object_id')
    associated_server = models.ForeignKey(Server, on_delete=models.SET_NULL, null=True, blank=True, related_name='server_credentials')
    associated_service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True, related_name='service_credentials')

    def __str__(self):
        return self.cred_name



# Join Table for Server and Service
class ServerService(models.Model):
    server = models.ForeignKey(Server, on_delete=models.SET_NULL, null=True)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ('server', 'service')

class ServiceCredential(models.Model):
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True)
    credential = models.ForeignKey(Credential, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ('service', 'credential')

    def __str__(self):
        return f"{self.service.name} - {self.credential.cred_name if self.credential else 'No Credential'}"

class ServerCredential(models.Model):
    server = models.ForeignKey(Server, on_delete=models.SET_NULL, null=True)
    credential = models.ForeignKey(Credential, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ('server', 'credential')

    def __str__(self):
        return f"{self.server.name} - {self.credential.cred_name if self.credential else 'No Credential'}"
