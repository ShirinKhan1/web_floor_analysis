# Generated by Django 5.0.3 on 2024-04-25 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('float', '0011_float_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='float',
            name='address',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='float',
            name='name',
            field=models.CharField(max_length=200, null=True),
        ),
    ]