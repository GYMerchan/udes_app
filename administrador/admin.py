from django.contrib import admin

from .models import Sitio, Reserva

# Register your models here. Administrador is 12345678

class SitioAdmin(admin.ModelAdmin):
    list_display = ["lugar_sitio", "aforo_maximo", "max_horas_diarias"]
    list_editable = ["aforo_maximo"]
    search_fields = ["lugar_sitio"]
    list_filter = ["lugar_sitio", "max_horas_diarias"]
    list_per_page = 1
    



admin.site.register(Sitio, SitioAdmin)
admin.site.register(Reserva)
