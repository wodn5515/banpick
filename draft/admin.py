from django.contrib import admin
from .models import Draft, Champion

# Register your models here.

class DraftAdmin(admin.ModelAdmin):
    list_display = ('match_name', 'date',)
    list_display_link = ('match_name',)

class ChampionAdmin(admin.ModelAdmin):
    list_display = ('name', 'keyword', 'no',)
    list_display_links = ('name',)
    ordering = ['id']


admin.site.register(Draft, DraftAdmin)
admin.site.register(Champion, ChampionAdmin)