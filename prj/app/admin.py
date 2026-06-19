from django.contrib import admin

from .models import Technique, TechniqueStat, Training


class TechniqueStatInline(admin.TabularInline):
    model = TechniqueStat
    extra = 1
    autocomplete_fields = ["technique"]


@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "date",
        "start_time",
        "duration",
        "wins",
        "losses",
        "draws",
    )
    list_filter = ("date", "user")
    search_fields = ("user__username", "user__email", "notes")
    date_hierarchy = "date"
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
    autocomplete_fields = ["training", "technique"]