from django.db import models

# Create your models here.
class Weapon(models.Model):
    weapon_name = models.CharField(max_length=15)
    user_name = models.CharField(max_length=100)
    weapon_trainer = models.CharField(max_length=100)
    weapon_available = models.IntegerField(null=True,blank=True)
    
    def __str__(self):
        return self.weapon_name 