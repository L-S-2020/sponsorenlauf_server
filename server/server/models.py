from django.db import models
from django.utils.crypto import get_random_string
import time

# Create your models here.
class Student(models.Model):
    code = models.CharField(max_length=6, primary_key=True, unique=True)
    name = models.CharField(max_length=200)
    lastseen = models.FloatField(default=time.time())
    kilometer = models.IntegerField(default=0)

    def __str__(self):
        return self.code

class School(models.Model):
    kilometer = models.IntegerField(default=0)

    def __str__(self):
        return str(self.kilometer)

class Runde(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    number = models.IntegerField()
    endtime = models.TimeField(auto_now_add=True)
    time = models.CharField(max_length=200)

    def __str__(self):
        return str(self.number)

class key(models.Model):
    key = models.CharField(max_length=200, primary_key=True, unique=True, default=get_random_string(length=32))
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.key