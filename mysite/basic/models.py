from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class school_user(models.Model):
   user = models.OneToOneField(User,related_name="school_user",on_delete=models.CASCADE)
   email =  models.CharField(max_length=200)
   role =  models.CharField(max_length=200,default="student")


   def __str__(self):
      return self.user.username
