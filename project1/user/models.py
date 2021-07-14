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
