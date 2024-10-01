from django.contrib.auth.models import AbstractUser
from django.db import models
# from django.contrib.auth.models import User

ROLE_CHOICES = (
        ('normal_user', 'Normal User'),
        ('volunteer_team', 'Volunteer Team'),
    )

class CustomUser(AbstractUser):
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='normal_user')
 

    
