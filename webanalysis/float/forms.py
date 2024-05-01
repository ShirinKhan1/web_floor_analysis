from django import forms
from float.choice_for_forms import *

class FloatArea(forms.Form):
    link = forms.URLField()


class Ai_calc(forms.Form):
    price = forms.IntegerField(min_value=0)
    cnt_room = forms.IntegerField(min_value=0)
    floor = forms.IntegerField(min_value=0)
    max_floor = forms.IntegerField(min_value=0)
    living_area = forms.FloatField(min_value=0)
    total_area = forms.FloatField(min_value=0)
    kitchen_area = forms.FloatField(min_value=0)
    year = forms.IntegerField(min_value=0)
    ceiling = forms.FloatField(min_value=0)
    cargo_el = forms.IntegerField(min_value=0)
    passenger_el = forms.IntegerField(min_value=0)
    balkon = forms.IntegerField(min_value=0)
    lodge = forms.IntegerField(min_value=0)
    finishing = forms.ChoiceField(choices=FINISHING)
    garbage = forms.BooleanField()
    gas = forms.ChoiceField(choices=GAS)
    heating = forms.ChoiceField(choices=HEATING)
    parking = forms.ChoiceField(choices=PARKING)
    reapair = forms.ChoiceField(choices=REPAIR)
    window = forms.ChoiceField(choices=WINDOW)
    credit = forms.BooleanField()
    deal = forms.ChoiceField(choices=DEAL)
    typeofhousing = forms.ChoiceField(choices=TYPEOFHOUSING)
    typeofhouse = forms.ChoiceField(choices=TYPEOFHOUSE)
    address = forms.CharField()