from django.contrib.auth.models import User
from django.db import models


class Float(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    link = models.URLField(max_length=100, unique=True)
    price = models.IntegerField(null=True)
    price2 = models.IntegerField(null=True)
    cntroom = models.IntegerField(null=True)
    floor = models.IntegerField(null=True)
    maxfloor = models.IntegerField(null=True)
    livingarea = models.FloatField(null=True)
    totalarea = models.FloatField(null=True)
    kitchenarea = models.FloatField(null=True)
    # ceiling_height = models.FloatField(null=True)
    year = models.IntegerField(null=True)
    credit = models.CharField(max_length=100, null=True)
    lavatory = models.CharField(max_length=100, null=True)
    ceiling = models.FloatField(null=True)  # высотка потолков
    balkonlodge = models.CharField(max_length=100, null=True)
    deal = models.CharField(max_length=100, null=True)
    window = models.CharField(max_length=100, null=True)
    repair = models.CharField(max_length=100, null=True)
    finishing = models.CharField(max_length=100, null=True)
    typeofhousing = models.CharField(max_length=100, null=True)
    elevator = models.CharField(max_length=100, null=True)
    typeofhouse = models.CharField(max_length=100, null=True)
    parking = models.CharField(max_length=100, null=True)
    heating = models.CharField(max_length=100, null=True)
    garbage = models.CharField(max_length=100, null=True)
    gas = models.CharField(max_length=100, null=True)


# class Type_of_housing(models.Model):
#     type_of_housing_id = models.IntegerField(primary_key=True)
#     value = models.CharField(max_length=100, unique=True)
#
#
# class Deal(models.Model):
#     deal_id = models.IntegerField(primary_key=True)
#     value = models.CharField(max_length=100, unique=True)
#
#
# class Window(models.Model):
#     window_id = models.IntegerField(primary_key=True)
#     value = models.CharField(max_length=100, unique=True)
#
#
# class Repair(models.Model):
#     repair_id = models.IntegerField(primary_key=True)
#     value = models.CharField(max_length=100, unique=True)
#
#
# class Finishing(models.Model):
#     Finishing_id = models.IntegerField(primary_key=True)
#     value = models.CharField(max_length=100, unique=True)
#
#
# class TypeOfHouse(models.Model):
#     Type_of_house_id = models.IntegerField(primary_key=True)
#     value = models.CharField(max_length=100, unique=True)
#
#
# class Parking(models.Model):
#     Parking_id = models.IntegerField(primary_key=True)
#     value = models.CharField(max_length=100, unique=True)
#
#
# class Heating(models.Model):
#     Heating_id = models.IntegerField(primary_key=True)
#     value = models.CharField(max_length=100, unique=True)
#
#
# class Garbage(models.Model):
#     Garbage_id = models.IntegerField(primary_key=True)
#     value = models.CharField(max_length=100, unique=True)
#
#
# class Gas(models.Model):
#     Gas_id = models.IntegerField(primary_key=True)
#     value = models.CharField(max_length=100, unique=True)
#
#
# class Img(models.Model):
#     id_float = models.IntegerField()
#     url = models.CharField(max_length=200, unique=True)


# class User(models.Model):
#     id = models.IntegerField(primary_key=True)
#     name = models.CharField(max_length=40)
#     surname = models.CharField(max_length=40)
#     msisdn = models.CharField(max_length=11)
#     email = models.CharField(max_length=100)
#     created = models.DateTimeField(auto_now_add=True)


class History(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    float = models.ForeignKey('Float', on_delete=models.CASCADE)
    method = models.CharField(max_length=50)
    create_date_dttm = models.DateField(null=True)
    linkarea = models.ForeignKey('LinkArea', on_delete=models.CASCADE, null=True)


class LinkArea(models.Model):
    id = models.AutoField(primary_key=True)
    link = models.URLField(null=True, max_length=3000, unique=True)


class AddresCoord(models.Model):
    id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=200, unique=True)
    width = models.FloatField(null=True)
    long = models.FloatField(null=True)
