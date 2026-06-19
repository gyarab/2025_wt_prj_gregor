from django.contrib import admin

from .models import Technique, TechniqueStat, Training, TrainingResult


admin.site.site_header = "FightLog Admin"
admin.site.site_title = "FightLog"
admin.site.index_title = "Správa tréninkového deníku"


class TrainingResultInline(admin.TabularInline):
    model = TrainingResult
    extra = 1
    autocomplete_fields = ["technique"]
    fields = ("result_type", "technique", "count")


class TechniqueStatInline(admin.TabularInline):
    model = TechniqueStat
    extra = 1
    autocomplete_fields = ["technique"]
    fields = ("technique", "count")


@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "user",
        "date",
        "duration",
        "wins",
        "losses",
        "draws",
        "total_sparrings",
    )
    list_filter = ("date", "user")
    search_fields = ("title", "user__username", "notes")
    date_hierarchy = "date"
    ordering = ("-date", "-start_time")
    inlines = [TrainingResultInline, TechniqueStatInline]


@admin.register(Technique)
class TechniqueAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(TrainingResult)
class TrainingResultAdmin(admin.ModelAdmin):
    list_display = ("id", "training", "result_type", "technique", "count")
    list_filter = ("result_type", "technique", "training__date")
    search_fields = ("training__title", "technique__name")
    autocomplete_fields = ["training", "technique"]


@admin.register(TechniqueStat)
class TechniqueStatAdmin(admin.ModelAdmin):
    list_display = ("id", "training", "technique", "count")
    list_filter = ("technique", "training__date")
    search_fields = ("technique__name", "training__title")
    autocomplete_fields = ["training", "technique"]