# Generated by Django 4.2.16 on 2024-09-10 21:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('site_setup', '0003_alter_sitesetup_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='menulink',
            name='site_setup',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='site_setup.sitesetup'),
        ),
    ]
