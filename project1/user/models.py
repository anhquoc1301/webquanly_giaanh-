from django.db import models
from  django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    name=models.CharField(max_length=50)
    phone=models.CharField(max_length=15)
    position=models.CharField(max_length=30)
    roll_choice = (('Admin', 'Admin'), ('Người Xem', 'Người Xem'), ('Người Báo Cáo', 'Người Báo Cáo'))
    roll=models.CharField(max_length=20, choices=roll_choice, default='')
    USERNAME_FIELD = 'username'



class Carmanagement(models.Model):
    # create_at = models.DateTimeField(auto_now_add=True)
    car_number=models.CharField(max_length=15)
    mass=models.CharField(max_length=10)
    driver=models.CharField(max_length=50)
    company=models.CharField(max_length=50)



class FileExcel_Carmanagement(models.Model):
    car_number=models.CharField(max_length=15)
    mass=models.CharField(max_length=10)
    driver=models.CharField(max_length=50)
    company=models.CharField(max_length=50)