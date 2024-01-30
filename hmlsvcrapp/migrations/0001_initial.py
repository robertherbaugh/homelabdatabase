# Generated by Django 3.2.23 on 2024-01-25 23:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Credential',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('last_updated', models.DateField()),
                ('mfa_enabled', models.BooleanField()),
                ('mfa_source', models.CharField(choices=[('Phone', 'Phone'), ('iCloud', 'iCloud Passwords'), ('Bitwarden', 'Bitwarden Passwords'), ('None', 'Not configured/available')], max_length=50)),
                ('sso', models.BooleanField()),
                ('account_type', models.CharField(choices=[('Root', 'Root'), ('User', 'User'), ('Admin', 'Admin'), ('Other', 'Other')], max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Network',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('vlan_id', models.IntegerField()),
                ('ip_space', models.CharField(max_length=18)),
                ('subnet_mask', models.CharField(max_length=18)),
            ],
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('ip_address', models.CharField(max_length=15)),
                ('location', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('type', models.CharField(choices=[('VM', 'Virtual Machine'), ('Docker', 'Docker'), ('Physical', 'Physical'), ('LXC', 'Linux Container'), ('Other', 'Other')], max_length=50)),
                ('os', models.CharField(choices=[('Debian', 'Debian'), ('Ubuntu', 'Ubuntu'), ('Windows', 'Windows'), ('OtherLinux', 'Other Linux'), ('macOS', 'macOS'), ('Other', 'Other')], max_length=50)),
                ('network', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='servers', to='hmlsvcrapp.network')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('port', models.IntegerField()),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive'), ('Decomissioned', 'Decomissioned')], max_length=50)),
                ('ip', models.CharField(max_length=15)),
                ('wazuh_agent_installed', models.BooleanField()),
                ('fqdn', models.CharField(max_length=255)),
                ('cloudflare_proxy_configured', models.BooleanField()),
                ('reverse_proxy_configured', models.BooleanField()),
                ('ldn', models.CharField(max_length=255)),
                ('dns_configured', models.BooleanField()),
                ('credentials', models.ManyToManyField(related_name='services', to='hmlsvcrapp.Credential')),
                ('server', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services', to='hmlsvcrapp.server')),
            ],
        ),
        migrations.CreateModel(
            name='ServiceCredential',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('credential', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hmlsvcrapp.credential')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hmlsvcrapp.service')),
            ],
            options={
                'unique_together': {('service', 'credential')},
            },
        ),
        migrations.CreateModel(
            name='ServerService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('server', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hmlsvcrapp.server')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hmlsvcrapp.service')),
            ],
            options={
                'unique_together': {('server', 'service')},
            },
        ),
    ]