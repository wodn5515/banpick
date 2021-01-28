from django.contrib import admin
from .models import Draft, Champion
from .forms import DraftChangeForm

# Register your models here.

@admin.register(Draft)
class DraftAdmin(admin.ModelAdmin):
    list_display = ('match_name', 'date', "timer", "banpick_final")
    list_display_link = ('match_name',)
    form = DraftChangeForm

@admin.register(Champion)
class ChampionAdmin(admin.ModelAdmin):
    list_display = ('name', 'no')
    list_display_links = ('name',)
    ordering = ['id']

