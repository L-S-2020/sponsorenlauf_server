from django.http import JsonResponse
from django.shortcuts import render
import time
from .models import Student, Runde, School, key
from django.utils import timezone, dateformat
from django.contrib.auth.models import User


# Create your views here.
def scanned(request, code):
    authorization = request.META.get('HTTP_AUTHORIZATION', None)
    if key.objects.get(key=authorization) is not None:
        schüler = Student.objects.get(code=code)
        if time.time()-schüler.lastseen > 135:
            schüler.kilometer += 1
            runde = Runde.objects.create(student=schüler, number=schüler.kilometer, time=time.time()-schüler.lastseen)
            schüler.save()
            schüler.lastseen = time.time()
            schüler.save()
            gesamt = School.objects.get()
            gesamt.kilometer += 1
            gesamt.save()
            return JsonResponse({"status": "ok", "kilometer": schüler.kilometer, "name": schüler.name})
        else:
            return JsonResponse({"status": "zu schnell", "name": schüler.name})
    else:
        return JsonResponse({"status": "unauthorized"})

def create(request, name):
    authorization = request.META.get('HTTP_AUTHORIZATION', None)
    if key.objects.get(key=authorization) is not None:
        random_number = User.objects.make_random_password(length=6, allowed_chars='1234567890')
        while Student.objects.filter(code=random_number):
            random_number = User.objects.make_random_password(length=6, allowed_chars='1234567890')
    
        schüler = Student(code=random_number, name=name, lastseen=time.time())
        schüler.save()
        return JsonResponse({"status": "ok", "code": schüler.code, "name": schüler.name})
    else:
        return JsonResponse({"status": "unauthorized"})
    

def main(request):
    print(Student.objects.all().count())
    return render(request, "index.html", {'schüler': Student.objects.all().count(), 'kilometer': School.objects.get().kilometer})

def stats(request, code):
    schüler = Student.objects.get(code=code)
    runden = Runde.objects.filter(student=schüler)
    return render(request, "stats.html")

def leaderboard(request):
    kilometer = School.objects.get().kilometer
    lauf = Runde.objects.order_by("time")[5]
    meiste_kilometer = Student.objects.order_by("kilometer")[5]
    return render(request, "leaderboard.html")

def start(request):
    authorization = request.META.get('HTTP_AUTHORIZATION', None)
    if key.objects.get(key=authorization) is not None:
        schüler = Student.objects.all()
        for i in schüler:
            i.kilometer = 0
            i.lastseen = time.time()
            i.save()
        gesamt = School.objects.get()
        gesamt.kilometer = 0
        gesamt.save()
        Runde.objects.all().delete()
        return JsonResponse({"status": "ok"})
    else:
        return JsonResponse({"status": "unauthorized"})

def test(request):
    authorization = request.META.get('HTTP_AUTHORIZATION', None)
    if key.objects.get(key=authorization) is not None:
        return JsonResponse({"status": "ok"})
    else:
        return JsonResponse({"status": "unauthorized"})