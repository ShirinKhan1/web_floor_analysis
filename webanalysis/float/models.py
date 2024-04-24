from django.db import models


class Float(models.Model):
    id = models.AutoField(primary_key=True)
    link = models.URLField(max_length=100, unique=True)
    price = models.IntegerField()
    cnt_room = models.IntegerField()
    floor = models.IntegerField()
    max_floor = models.IntegerField()
    living_area = models.FloatField(null=True)
    total_area = models.FloatField()
    kitchen_area = models.FloatField(null=True)
    ceiling_height = models.FloatField(null=True)
    year = models.IntegerField(null=True)
    ceiling = models.FloatField(null=True)    # высотка потолков
    balkon_lodge = models.ForeignKey('BalkonLodge', on_delete=models.CASCADE, default=0)
    window = models.ForeignKey('Window', on_delete=models.CASCADE, default=0)
    repair = models.ForeignKey('Repair', on_delete=models.CASCADE, default=0)
    finishing = models.ForeignKey('Finishing', on_delete=models.CASCADE, default=0)
    elevator = models.ForeignKey('Elevator', on_delete=models.CASCADE, default=0)
    type_of_house = models.ForeignKey('TypeOfHouse', on_delete=models.CASCADE, default=0)
    parking = models.ForeignKey('Parking', on_delete=models.CASCADE, default=0)
    heating = models.ForeignKey('Heating', on_delete=models.CASCADE, default=0)
    garbage = models.ForeignKey('Garbage', on_delete=models.CASCADE, default=0)
    gas = models.ForeignKey('Gas', on_delete=models.CASCADE, default=0)


class BalkonLodge(models.Model):
    balkon_lodge_id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, unique=True)


class Window(models.Model):
    window_id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, unique=True)


class Repair(models.Model):
    repair_id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, unique=True)


class Finishing(models.Model):
    Finishing_id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, unique=True)


class Elevator(models.Model):
    Elevator_id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, unique=True)


class TypeOfHouse(models.Model):
    Type_of_house_id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, unique=True)


class Parking(models.Model):
    Parking_id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, unique=True)


class Heating(models.Model):
    Heating_id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, unique=True)


class Garbage(models.Model):
    Garbage_id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, unique=True)


class Gas(models.Model):
    Gas_id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, unique=True)


class Img(models.Model):
    id_float = models.IntegerField()
    url = models.CharField(max_length=200, unique=True)


class User(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=40)
    surname = models.CharField(max_length=40)
    msisdn = models.CharField(max_length=11)
    email = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)


class History(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    float = models.ForeignKey('Float', on_delete=models.CASCADE)
    method = models.CharField(max_length=50)
