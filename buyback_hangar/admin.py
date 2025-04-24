from django.contrib import admin
from .models import TrackedHangarLocation

@admin.register(TrackedHangarLocation)
class TrackedHangarLocationAdmin(admin.ModelAdmin):
    list_display = ('location_id', 'name', 'enabled')
    list_filter = ('enabled',)
    search_fields = ('name',)
