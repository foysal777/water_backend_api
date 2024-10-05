from rest_framework import serializers
from django.db import models
from django.conf import settings
from account .models import CustomUser

ROLE_CHOICES = (
        ('normal_user', 'Normal User'),
        ('volunteer_team', 'Volunteer Team'),
    )


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    location = models.CharField(max_length=30 , default='dhaka')
    image_url = models.CharField(max_length=255, null=True, blank=True) 
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='normal_user')
    
    
    
    def __str__(self):
        return self.title
    
    
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.created_by} on {self.post}"
    
    
    
    
class Team(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name




class Member(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE , default = 1)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254 ,default='help@gmail.com')
    contact_number = models.CharField(max_length=15 , default=9663324) 
    team = models.ForeignKey(Team, related_name='members', on_delete=models.CASCADE)
    is_pending = models.BooleanField(default=False)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='normal_user')

    


    def __str__(self):
        return self.name



class Volunteer(models.Model):
    team_id = models.IntegerField()
    first_name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return f"{self.first_name} ({self.email})"
    