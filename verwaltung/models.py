from django.db import models
from django.utils.crypto import get_random_string
import time

# Create your models here.
class Student(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=6, unique=True)
    vorname = models.CharField(max_length=200)
    familienname = models.CharField(max_length=200)
    shortname = models.CharField(max_length=200)
    lastseen = models.FloatField(default=time.time())
    klasse = models.ForeignKey('Klasse', on_delete=models.CASCADE)

    def __str__(self):
        return self.shortname
    
    def anzahl_runden(self):
        return Runde.objects.filter(student=self).count()
    
    def anwesend(self):
        return self.anzahl_runden() > 0
    
    def meter(self):
        return self.anzahl_runden() * 550
    
    def name(self):
        vorname_teil = self.vorname.split(" ")[0] # nur der erste Vorname
        return vorname_teil + " " + self.familienname
    
    def name_ganz(self):
        return self.vorname + " " + self.familienname

class Klasse(models.Model):
    name = models.CharField(max_length=100)
    shortname = models.CharField(max_length=15)
    stufe = models.CharField(max_length=100) # "unter" (5-7), "mittel" (8-10), "ober" (KS1 und KS2)

    def __str__(self):
        return self.name
    
    def anzahl_runden(self):
        return Runde.objects.filter(student__klasse=self).count()
    
    def avg_runden(self):
        # anzahl schüler mit mind. 1 runde
        anwesende_schüler = Student.objects.filter(klasse=self, runde__isnull=False).distinct().count()
        runden = self.anzahl_runden()
        if anwesende_schüler == 0: # catch division by zero
            return 0
        return runden/anwesende_schüler

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
