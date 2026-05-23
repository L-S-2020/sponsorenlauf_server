from django.contrib import admin
from django.db.models import Count, F, FloatField, ExpressionWrapper, Case, When, Value, Q
from django.db.models.functions import Cast
from .models import Student, Runde, key, Klasse


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name_ganz', 'klasse', 'code', 'anzahl_runden']
    list_filter = ('klasse',)
    search_fields = ('vorname', 'familienname', 'code')

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(runden_count=Count('runde'))

    @admin.display(ordering='runden_count', description='Anzahl Runden')
    def anzahl_runden(self, obj):
        return obj.runden_count


@admin.register(Klasse)
class KlasseAdmin(admin.ModelAdmin):
    list_display = ['name', 'stufe', 'schüler', 'anwesende_schüler', 'anzahl_runden', 'avg_runden']
    search_fields = ('name', 'stufe')
    list_filter = ('stufe',)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            schueler_count=Count('student', distinct=True),
            anwesende_count=Count('student', filter=Q(student__runde__isnull=False), distinct=True),
            runden_count=Count('student__runde'),
        ).annotate(
            avg_runden_val=Case(
                When(anwesende_count=0, then=Value(0.0)),
                default=ExpressionWrapper(
                    Cast(F('runden_count'), FloatField()) / F('anwesende_count'),
                    output_field=FloatField(),
                ),
                output_field=FloatField(),
            )
        )

    @admin.display(ordering='schueler_count', description='Schüler')
    def schüler(self, obj):
        return obj.schueler_count

    @admin.display(ordering='anwesende_count', description='Anwesende Schüler')
    def anwesende_schüler(self, obj):
        return obj.anwesende_count

    @admin.display(ordering='runden_count', description='Anzahl Runden')
    def anzahl_runden(self, obj):
        return obj.runden_count

    @admin.display(ordering='avg_runden_val', description='Ø Runden')
    def avg_runden(self, obj):
        return round(obj.avg_runden_val, 1) if obj.avg_runden_val else 0


@admin.register(Runde)
class RundeAdmin(admin.ModelAdmin):
    list_display = ['student', 'number', 'time']
    list_filter = ('student__klasse',)
    search_fields = ('student__vorname', 'student__familienname', 'student__code')

@admin.register(key)
class KeyAdmin(admin.ModelAdmin):
    list_display = ['key', 'name']
    search_fields = ('key', 'name')

admin.site.site_header = "Sponsorenlauf 2026"
admin.site.site_title = "Sponsorenlauf 2026 Backend"
