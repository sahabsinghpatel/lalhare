from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.IntegerField (blank=False)
    birth_date = models.DateField(null=True, blank=True)
    wallet_bal = models.IntegerField(default=0)
    upi = models.CharField(blank=True, max_length=39)
    bank_ac = models.CharField(max_length=50, blank=True, default='*************XX')
    bank_ifsc = models.CharField(max_length=20, blank=True)
    varified = models.BooleanField(default=False)

class Orders(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class History(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    trade_hist=models.CharField(blank=False, max_length=100)

class MSG(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    msg = models.CharField(blank=False, max_length=100)

class Temp_User(models.Model):
    username=models.CharField(max_length=100, blank=True)
    email=models.EmailField(max_length=100)
    password=models.CharField(max_length=40, blank=True)
    otp=models.IntegerField()
    token=models.CharField(max_length=65)
    time=models.TimeField(auto_now_add=True)
