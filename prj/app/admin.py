from django.contrib import admin
from .models import Training, Technique, TechniqueStat


class TechniqueStatInline(admin.TabularInline):
    model = TechniqueStat
    extra = 1


@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "date", "start_time", "duration", "wins", "losses", "draws")
    list_filter = ("date", "user")
    search_fields = ("user__username", "notes")
    inlines = [TechniqueStatInline]


@admin.register(Technique)
class TechniqueAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(TechniqueStat)
class TechniqueStatAdmin(admin.ModelAdmin):
    list_display = ("id", "training", "technique", "count")
    list_filter = ("technique", "training__date")
    search_fields = ("technique__name", "training__user__username")