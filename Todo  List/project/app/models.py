from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User
from  django.contrib.auth.models import AbstractUser
from django.utils import timezone

class customuser(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    is_user = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    def has_admin_permission(self):
        return self.is_admin

class Category(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(
        customuser,
        on_delete=models.CASCADE,
        related_name='categories'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class Task(models.Model):
    STATUS_CHOICES = (('running', 'Running'),('completed', 'Completed'),)
    PRIORITY_CHOICES = (('low', 'Low'),('medium', 'Medium'),('high', 'High'),)
    user = models.ForeignKey(customuser,on_delete=models.CASCADE,related_name='tasks')
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,blank=True,related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='running')
    due_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title



class UserOTP(models.Model):
    user = models.ForeignKey(customuser, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=3)