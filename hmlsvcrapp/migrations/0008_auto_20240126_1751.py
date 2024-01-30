# Generated by Django 3.2.23 on 2024-01-26 23:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hmlsvcrapp', '0007_auto_20240126_1622'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='credentials',
            field=models.ManyToManyField(blank=True, related_name='services', to='hmlsvcrapp.Credential'),
        ),
        migrations.AlterField(
            model_name='service',
            name='cred_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='services_name', to='hmlsvcrapp.credential', to_field='cred_name'),
        ),
    ]
