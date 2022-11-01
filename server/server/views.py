from django.http import JsonResponse
from django.shortcuts import render
from .models import Student, Runde, School, key
from django.utils import timezone, dateformat


# Create your views here.
def scanned(request, code):
    authorization = request.META.get('HTTP_AUTHORIZATION', None)
    if key.objects.get(key=authorization) is not None:
        schüler = Student.objects.get(code=code)
        schüler.kilometer += 1
        runde = Runde.objects.create(student=schüler, number=schüler.kilometer, time=timezone.now()-schüler.lastseen())
        schüler.save()
        schüler.lastseen = timezone.now()
        schüler.save()
        gesamt = School.objects.get()
        gesamt.kilometer += 1
        gesamt.save()
        return JsonResponse({"status": "ok", "kilometer": schüler.kilometer, "name": schüler.name})
    else:
        return JsonResponse({"status": "unauthorized"})

def create(request, name):
    authorization = request.META.get('HTTP_AUTHORIZATION', None)
    if key.objects.get(key=authorization) is not None:
        random_number = Student.objects.make_random_password(length=6, allowed_chars='1234567890')
        while Student.objects.filter(code=random_number):
            random_number = Student.objects.make_random_password(length=6, allowed_chars='1234567890')
    
        schüler = Student(code=random_number, name=name,)
        schüler.save()
        return JsonResponse({"status": "ok", "code": schüler.code, "name": schüler.name})
    else:
        return JsonResponse({"status": "unauthorized"})
    

def main(request):
    return render(request, "main.html")

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
            i.lastseen = timezone.now()
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