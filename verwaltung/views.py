from django.db.models import Count, FloatField, ExpressionWrapper, F, Q, Case, When, Value
from django.db.models.functions import Cast
from django.http import JsonResponse
from django.shortcuts import render, redirect
import time
from .models import Student, Runde, key, Klasse
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
        seconds = time.time()-schüler.lastseen
        if seconds > 0: # Change to 40 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            rundennummer = schüler.anzahl_runden() + 1
            zeit = timedelta(seconds=seconds)
            runde = Runde.objects.create(student=schüler, number=rundennummer, time=zeit)
            runde.save()
            schüler.lastseen = time.time()
            schüler.save()
            return JsonResponse({"status": "ok", "kilometer": schüler.anzahl_runden(), "name": schüler.name()})
        else:
            return JsonResponse({"status": "zu schnell", "name": schüler.name()})
    else:
        return JsonResponse({"status": "unauthorized"})

def create(request, vorname, familienname, shortname, klasse, code):
    authorization = request.META.get('HTTP_AUTHORIZATION', None)
    if key.objects.get(key=authorization) is not None:
        if not Klasse.objects.filter(shortname=klasse).exists():
            return JsonResponse({"status": "klasse nicht gefunden"})
        klasse = Klasse.objects.get(shortname=klasse)
        schüler = Student(code=code, vorname=vorname, familienname=familienname, shortname=shortname, klasse=klasse, lastseen=time.time())
        schüler.save()
        return JsonResponse({"status": "created", "code": schüler.code, "name": schüler.name(), "klasse": schüler.klasse.name})
    return JsonResponse({"status": "unauthorized"})

def createklasse(request, name):
    authorization = request.META.get('HTTP_AUTHORIZATION', None)
    if key.objects.get(key=authorization) is not None:
        klasse = Klasse(shortname=name)
        klasse.name = name.upper()
        if name.startswith("5") or name.startswith("6") or name.startswith("7"):
            klasse.stufe = "unter"
        elif name.startswith("8") or name.startswith("9") or name.startswith("10"):
            klasse.stufe = "mittel"
        elif name.startswith("K"):
            klasse.stufe = "ober"
        else:
            klasse.stufe = "sonstige"
        klasse.save()
        return JsonResponse({"status": "created", "name": klasse.shortname})
    return JsonResponse({"status": "unauthorized"})

def main(request):
    if request.method == "POST":
        form = Codeform(request.POST)
        if form.is_valid():
            code = form.cleaned_data["code"]
            return redirect("stats", code=code)
    else:
        form = Codeform()
    return render(request, "index.html", {'schüler': Student.objects.all().count(), 'kilometer': Runde.objects.all().count(), 'form': form})

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
        platz = Student.objects.annotate(runden_count=Count('runde')).filter(runden_count__gt=schüler.anzahl_runden()).count() + 1
        return render(request, "stats.html", {'schüler': schüler, 'runden': runden, 'platz': platz})
    else:
        messages.error(request, 'Der eingegebene Code ist ungültig.')
        return redirect("main")


def leaderboard(request):
    return render(request, "leaderboard.html")

def start(request):
    authorization = request.META.get('HTTP_AUTHORIZATION', None)
    if key.objects.get(key=authorization) is not None:
        schüler = Student.objects.all()
        for i in schüler:
            i.lastseen = time.time()
            i.save()
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
    anzahl_runden = Runde.objects.count()
    anzahl_kilometer = anzahl_runden * 0.55 # Ja ich weiß, dass ich das auch im Client berechnen könnte, aber so ist es einfacher später zu ändern
    ranking_schüler = Student.objects.annotate(runden_count=Count('runde')).order_by('-runden_count', 'lastseen')[:16]
    json_schüler = []
    for i in ranking_schüler:
        json_schüler.append({"name": i.name(), "klasse": i.klasse.name, "runden": i.anzahl_runden(), })
    
    def ranking_für_stufe(stufe):
        return (
            Klasse.objects.filter(stufe=stufe)
            .annotate(
                runden_count=Count('student__runde'),
                anwesende=Count('student', filter=Q(student__runde__isnull=False), distinct=True),
            )
            .annotate(
                runden_avg=Case(
                    When(anwesende=0, then=Value(0.0)),
                    default=ExpressionWrapper(
                        Cast(F('runden_count'), FloatField()) / F('anwesende'),
                        output_field=FloatField(),
                    ),
                    output_field=FloatField(),
                )
            )
            .order_by('-runden_avg')[:8]
        )

    ranking_unterstufe = ranking_für_stufe("unter")
    json_unterstufe = [{"name": i.name, "avg_runden": round(i.runden_avg, 2)} for i in ranking_unterstufe]

    ranking_mittelstufe = ranking_für_stufe("mittel")
    json_mittelstufe = [{"name": i.name, "avg_runden": round(i.runden_avg, 2)} for i in ranking_mittelstufe]

    ranking_oberstufe = ranking_für_stufe("ober")
    json_oberstufe = [{"name": i.name, "avg_runden": round(i.runden_avg, 2)} for i in ranking_oberstufe]
    
    letzte_runden = Student.objects.order_by('-lastseen').filter(runde__isnull=False).distinct()[:8]
    json_letzte_runden = []
    for i in letzte_runden:
        json_letzte_runden.append({"name": i.name(), "klasse": i.klasse.name, "runden": i.anzahl_runden(), })

    return JsonResponse({"anzahl_runden": anzahl_runden, "anzahl_kilometer": anzahl_kilometer, "ranking_schüler": json_schüler, "ranking_unterstufe": json_unterstufe, "ranking_mittelstufe": json_mittelstufe, "ranking_oberstufe": json_oberstufe, "letzte_runden": json_letzte_runden})


def leaderboardapi_alt(request):
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
    meiste_kilometer = Student.objects.order_by("-kilometer", "lastseen")[:10]
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
    meiste_kilometer = Student.objects.order_by("-kilometer", "lastseen")[:10]
    for i in meiste_kilometer:
        dict_kilometer.append({"name": i.name, "kilometer": i.kilometer})
    return JsonResponse({"kilometer": kilometer, "klassen": dict_klassen, "meiste_kilometer": dict_kilometer, "status": "changed"})

def meter(request, code):
    if Student.objects.filter(code=code).exists():
        schüler = Student.objects.get(code=code)
        return JsonResponse({"status": "ok", "meter": schüler.kilometer})
    else:
        return JsonResponse({"status": "code nicht gefunden"})