# Generated by Django 5.0.3 on 2024-05-01 05:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('float', '0026_rename_linkid_history_linkarea'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='history',
            name='link',
        ),
    ]
