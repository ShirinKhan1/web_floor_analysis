# Generated by Django 5.0.3 on 2024-04-24 18:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BalkonLodge',
            fields=[
                ('balkon_lodge_id', models.IntegerField(primary_key=True, serialize=False)),
                ('value', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Elevator',
            fields=[
                ('Elevator_id', models.IntegerField(primary_key=True, serialize=False)),
                ('value', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Finishing',
            fields=[
                ('Finishing_id', models.IntegerField(primary_key=True, serialize=False)),
                ('value', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Garbage',
            fields=[
                ('Garbage_id', models.IntegerField(primary_key=True, serialize=False)),
                ('value', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Gas',
            fields=[
                ('Gas_id', models.IntegerField(primary_key=True, serialize=False)),
                ('value', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Heating',
            fields=[
                ('Heating_id', models.IntegerField(primary_key=True, serialize=False)),
                ('value', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Img',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_float', models.IntegerField()),
                ('url', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Parking',
            fields=[
                ('Parking_id', models.IntegerField(primary_key=True, serialize=False)),
                ('value', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Repair',
            fields=[
                ('repair_id', models.IntegerField(primary_key=True, serialize=False)),
                ('value', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TypeOfHouse',
            fields=[
                ('Type_of_house_id', models.IntegerField(primary_key=True, serialize=False)),
                ('value', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=40)),
                ('surname', models.CharField(max_length=40)),
                ('msisdn', models.CharField(max_length=11)),
                ('email', models.CharField(max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Window',
            fields=[
                ('window_id', models.IntegerField(primary_key=True, serialize=False)),
                ('value', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Float',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('link', models.URLField(max_length=100, unique=True)),
                ('price', models.IntegerField()),
                ('cnt_room', models.IntegerField()),
                ('floor', models.IntegerField()),
                ('max_floor', models.IntegerField()),
                ('living_area', models.FloatField(null=True)),
                ('total_area', models.FloatField()),
                ('kitchen_area', models.FloatField(null=True)),
                ('ceiling_height', models.FloatField(null=True)),
                ('year', models.IntegerField(null=True)),
                ('ceiling', models.FloatField(null=True)),
                ('balkon_lodge', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='float.balkonlodge')),
                ('elevator', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='float.elevator')),
                ('finishing', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='float.finishing')),
                ('garbage', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='float.garbage')),
                ('gas', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='float.gas')),
                ('heating', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='float.heating')),
                ('parking', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='float.parking')),
                ('repair', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='float.repair')),
                ('type_of_house', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='float.typeofhouse')),
                ('window', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='float.window')),
            ],
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('method', models.CharField(max_length=50)),
                ('float', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='float.float')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='float.user')),
            ],
        ),
    ]
