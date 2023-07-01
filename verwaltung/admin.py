from django.contrib import admin
from .models import Student, School, Runde, key, Klasse


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'klasse', 'code', 'kilometer']
    list_filter = ('klasse', 'kilometer')
    search_fields = ('name', 'code')

admin.site.register(School)
admin.site.register(Runde)
admin.site.register(key)
admin.site.register(Klasse)
