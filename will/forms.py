from django import forms
from .models import Weapon

class WeaponForm(forms.ModelForm):
    class Meta:
        model = Weapon
        fields = ["weapon_name","user_name", "weapon_trainer",]