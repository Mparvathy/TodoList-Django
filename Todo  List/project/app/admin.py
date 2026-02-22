from django.contrib import admin
from .models import  customuser,Task,Category,UserOTP

admin.site.register(customuser)
admin.site.register(Task)
admin.site.register(Category)
admin.site.register(UserOTP)