from django.contrib import admin
from .models import POI


@admin.register(POI)
class PoIAdmin(admin.ModelAdmin):
    list_display = (
        'internal_id',
        'name',
        'external_id',
        'category',
        'avg_rating',
    )

    search_fields = ('internal_id', 'external_id', 'name')  
    list_filter = ('category',)
    ordering = ('internal_id',)