# Generated by Django 5.0.3 on 2024-04-30 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('float', '0021_alter_history_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='history',
            name='link',
            field=models.URLField(max_length=3000, null=True),
        ),
    ]
