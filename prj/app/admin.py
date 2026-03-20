from django.contrib import admin
from .models import Training, Technique, TechniqueStat


@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = ("user", "date", "duration", "wins", "losses")
    list_filter = ("date", "user")
    search_fields = ("notes",)


@admin.register(Technique)
class TechniqueAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(TechniqueStat)
class TechniqueStatAdmin(admin.ModelAdmin):
    list_display = ("training", "technique", "count")