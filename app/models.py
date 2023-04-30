from django.db import models

# Create your models here.
class UserTable(models.Model):
    username=models.CharField(max_length=40)
    email=models.CharField(max_length=70)
    full_name=models.CharField(max_length=90)
    age=models.IntegerField(default=0)
    voiceRecorded=models.IntegerField(default=0)