# Generated by Django 5.0.3 on 2024-04-30 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('float', '0019_rename_date_history_create_date_dttm'),
    ]

    operations = [
        migrations.AddField(
            model_name='history',
            name='link',
            field=models.URLField(null=True),
        ),
    ]
