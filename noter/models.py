from django.db import models

# Create your models here.

class note(models.Model):
    username = models.CharField(max_length=50)
    note_name = models.CharField(max_length=50)
    note_text = models.CharField(max_length=100)
    date = models.CharField(max_length=50)
    fav = models.CharField(max_length=5, default="F")
