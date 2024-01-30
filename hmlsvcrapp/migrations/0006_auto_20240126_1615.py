# Generated by Django 3.2.23 on 2024-01-26 22:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hmlsvcrapp', '0005_auto_20240126_1613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='credential',
            name='associated_server',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='server_credentials', to='hmlsvcrapp.server'),
        ),
        migrations.AlterField(
            model_name='credential',
            name='associated_service',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='service_credentials', to='hmlsvcrapp.service'),
        ),
        migrations.AlterField(
            model_name='server',
            name='cred_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='servers', to='hmlsvcrapp.credential', to_field='cred_name'),
        ),
        migrations.AlterField(
            model_name='service',
            name='cred_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='services', to='hmlsvcrapp.credential', to_field='cred_name'),
        ),
    ]