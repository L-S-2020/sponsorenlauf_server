from django.conf import settings
from django.db import models
from django.utils import timezone

# Create your models here.
class Student(models.Model):
    code = models.CharField(max_length=6, primary_key=True)
    name = models.CharField(max_length=200)
    klassenstufe = models.IntegerField()
    klasse = models.CharField(max_length=1)
    lastseen = models.TimeField(auto_now=True)
    kilometer = models.IntegerField(default=0)

    def __str__(self):
        return self.code

class School(models.Model):
    kilometer = models.IntegerField(default=0)

    def __str__(self):
        return self.kilometer

class Runde(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    number = models.IntegerField()
    endtime = models.TimeField(auto_now_add=True)
    time = models.TimeField()

    def __str__(self):
        return self.number