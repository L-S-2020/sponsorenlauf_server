from django.http import JsonResponse
from django.shortcuts import render
from .models import Student, Runde, School
from django.utils import timezone, dateformat


# Create your views here.
def scanned(request, code):
    schüler = Student.objects.get(code=code)
    schüler.kilometer += 1
    runde = Runde(student=schüler, number=schüler.kilometer, time=schüler.lastseen()-timezone.now())
    schüler.save()
    schüler.lastseen = timezone.now()
    schüler.save()
    gesamt = School.objects.get()
    gesamt.kilometer += 1
    gesamt.save()
    return JsonResponse({"kilometer": schüler.kilometer, "name": schüler.name})

def create(request, name, klassenstufe, klasse):
    random_number = Student.objects.make_random_password(length=6, allowed_chars='1234567890')
    while Student.objects.filter(code=random_number):
        random_number = User.objects.make_random_password(length=6, allowed_chars='1234567890')
    
    schüler = Student(code=random_number, name=name, klassenstufe=klassenstufe, klasse=klasse)
    schüler.save()
    return JsonResponse({"code": schüler.code, "name": schüler.name})

def main(request):
    return render(request, "main.html")

def stats(request, code):
    schüler = Student.objects.get(code=code)
    runden = Runde.objects.filter(student=schüler)
    return render(request, "stats.html")
    