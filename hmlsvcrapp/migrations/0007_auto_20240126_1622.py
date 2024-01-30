# Generated by Django 3.2.23 on 2024-01-26 22:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hmlsvcrapp', '0006_auto_20240126_1615'),
    ]

    operations = [
        migrations.AlterField(
            model_name='credential',
            name='associated_server',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='server_credentials', to='hmlsvcrapp.server'),
        ),
        migrations.AlterField(
            model_name='credential',
            name='associated_service',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='service_credentials', to='hmlsvcrapp.service'),
        ),
        migrations.AlterField(
            model_name='server',
            name='cred_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='servers', to='hmlsvcrapp.credential', to_field='cred_name'),
        ),
        migrations.AlterField(
            model_name='server',
            name='network',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='servers', to='hmlsvcrapp.network'),
        ),
        migrations.AlterField(
            model_name='servercredential',
            name='credential',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hmlsvcrapp.credential'),
        ),
        migrations.AlterField(
            model_name='servercredential',
            name='server',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hmlsvcrapp.server'),
        ),
        migrations.AlterField(
            model_name='serverservice',
            name='server',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hmlsvcrapp.server'),
        ),
        migrations.AlterField(
            model_name='serverservice',
            name='service',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hmlsvcrapp.service'),
        ),
        migrations.AlterField(
            model_name='service',
            name='cred_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='services', to='hmlsvcrapp.credential', to_field='cred_name'),
        ),
        migrations.AlterField(
            model_name='service',
            name='network',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='services', to='hmlsvcrapp.network'),
        ),
        migrations.AlterField(
            model_name='service',
            name='server',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='services', to='hmlsvcrapp.server'),
        ),
        migrations.AlterField(
            model_name='servicecredential',
            name='credential',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hmlsvcrapp.credential'),
        ),
        migrations.AlterField(
            model_name='servicecredential',
            name='service',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hmlsvcrapp.service'),
        ),
    ]