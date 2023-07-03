from django.http import JsonResponse
from django.shortcuts import render, redirect
import time
from .models import Student, Runde, School, key, Klasse
from .forms import Codeform
from datetime import timedelta
from django.contrib import messages

last_kilometer = 0
# Create your views here.
#
def scanned(request, code):
    authorization = request.META.get('HTTP_AUTHORIZATION', None)
    if key.objects.get(key=authorization) is not None:
        schüler = Student.objects.get(code=code)
        if time.time()-schüler.lastseen > 50:
            schüler.kilometer += 0.5
            seconds = time.time()-schüler.lastseen
            minutes = timedelta(seconds=seconds)
            runde = Runde.objects.create(student=schüler, number=schüler.kilometer, time=minutes)
            runde.save()
            schüler.save()
            schüler.lastseen = time.time()
            schüler.save()
            gesamt = School.objects.get()
            gesamt.kilometer += 0.5
            gesamt.save()
            return JsonResponse({"status": "ok", "kilometer": schüler.kilometer, "name": schüler.name})
        else:
            return JsonResponse({"status": "zu schnell", "name": schüler.name})
    else:
        return JsonResponse({"status": "unauthorized"})

def create(request, name, klasse, code):
    authorization = request.META.get('HTTP_AUTHORIZATION', None)
    if key.objects.get(key=authorization) is not None:
        if not Klasse.objects.filter(name=klasse).exists():
            return JsonResponse({"status": "klasse nicht gefunden"})
        klasse = Klasse.objects.get(name=klasse)
        schüler = Student(code=code, name=name, klasse=klasse ,lastseen=time.time())
        schüler.save()
        return JsonResponse({"status": "created", "code": schüler.code, "name": schüler.name, "klasse": schüler.klasse.name})
    return JsonResponse({"status": "unauthorized"})

def createklasse(request, name):
    authorization = request.META.get('HTTP_AUTHORIZATION', None)
    if key.objects.get(key=authorization) is not None:
        klasse = Klasse(name=name)
        klasse.save()
        return JsonResponse({"status": "created", "name": klasse.name})
    return JsonResponse({"status": "unauthorized"})

def main(request):
    if request.method == "POST":
        form = Codeform(request.POST)
        if form.is_valid():
            code = form.cleaned_data["code"]
            return redirect("stats", code=code)
    else:
        form = Codeform()
    return render(request, "index.html", {'schüler': Student.objects.all().count(), 'kilometer': School.objects.get().kilometer, 'form': form})

# it gets the code of the student and returns the stats.html file
def stats(request, code):
    """
    It takes a request and a code, gets the student with that code, and then gets all the rounds that student has run.

    :param request: The request object
    :param code: The code of the student
    :return: The stats.html file is being returned.
    """
    if Student.objects.filter(code=code).exists():
        schüler = Student.objects.get(code=code)
        runden = Runde.objects.filter(student=schüler)
        platz = Student.objects.filter(kilometer__gt=schüler.kilometer).count() + 1
        return render(request, "stats.html", {'schüler': schüler, 'runden': runden, 'platz': platz})
    else:
        messages.error(request, 'Der eingegebene Code ist ungültig.')
        return redirect("main")


# it gets the 10 classes with the most kilometers and the 10 students with the most kilometers and returns the leaderboard.html file
def leaderboard(request):
    kilometer = School.objects.get().kilometer
    #get the 10 classes with the most kilometers
    klassen = Klasse.objects.order_by("-kilometer")[:10]
    meiste_kilometer = Student.objects.order_by("-kilometer")[:10]
    return render(request, "leaderboard.html", {'kilometer': kilometer, 'klassen': klassen, 'meiste_kilometer': meiste_kilometer})

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

def leaderboardapi(request):
    global last_kilometer
    kilometer = School.objects.get().kilometer
    if kilometer == last_kilometer:
        return JsonResponse({"status": "not changed"})
    # get the 10 classes with the most kilometers
    last_kilometer = kilometer
    dict_klassen = []
    klassen = Klasse.objects.order_by("-kilometer")[:10]
    for i in klassen:
        dict_klassen.append({"name": i.name, "kilometer": i.kilometer})
    dict_kilometer = []
    meiste_kilometer = Student.objects.order_by("-kilometer")[:10]
    for i in meiste_kilometer:
        dict_kilometer.append({"name": i.name, "kilometer": i.kilometer})
    return JsonResponse({"kilometer": kilometer, "klassen": dict_klassen, "meiste_kilometer": dict_kilometer, "status": "changed"})

def leaderboardforce(request):
    kilometer = School.objects.get().kilometer
    # get the 10 classes with the most kilometers
    dict_klassen = []
    klassen = Klasse.objects.order_by("-kilometer")[:10]
    for i in klassen:
        dict_klassen.append({"name": i.name, "kilometer": i.kilometer})
    dict_kilometer = []
    meiste_kilometer = Student.objects.order_by("-kilometer")[:10]
    for i in meiste_kilometer:
        dict_kilometer.append({"name": i.name, "kilometer": i.kilometer})
    return JsonResponse({"kilometer": kilometer, "klassen": dict_klassen, "meiste_kilometer": dict_kilometer, "status": "changed"})

