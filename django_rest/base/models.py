from django.db import models


# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    #id
    created = models.DateTimeField(auto_now_add=True)

