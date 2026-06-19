from django.contrib import admin

from .models import Technique, TechniqueStat, Training


admin.site.site_header = "FightLog Admin"
admin.site.site_title = "FightLog"
admin.site.index_title = "Správa tréninkového deníku"


class TechniqueStatInline(admin.TabularInline):
    model = TechniqueStat
    extra = 1
    autocomplete_fields = ["technique"]
    fields = ("technique", "count")


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
        "total_sparrings",
    )
    list_display_links = ("id", "user", "date")
    list_filter = ("date", "user")
    search_fields = ("user__username", "user__email", "notes")
    date_hierarchy = "date"
    ordering = ("-date", "-start_time")
    inlines = [TechniqueStatInline]

    fieldsets = (
        ("Základní informace", {
            "fields": ("user", "date", "start_time", "duration")
        }),
        ("Výsledky sparringů", {
            "fields": ("wins", "losses", "draws")
        }),
        ("Poznámky", {
            "fields": ("notes",)
        }),
    )

    def total_sparrings(self, obj):
        return obj.wins + obj.losses + obj.draws

    total_sparrings.short_description = "Celkem sparringů"


@admin.register(Technique)
class TechniqueAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "usage_count")
    list_display_links = ("id", "name")
    search_fields = ("name",)
    ordering = ("name",)

    def usage_count(self, obj):
        return obj.technique_stats.count()

    usage_count.short_description = "Počet použití v záznamech"


@admin.register(TechniqueStat)
class TechniqueStatAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "training",
        "technique",
        "count",
    )
    list_display_links = ("id", "training", "technique")
    list_filter = ("technique", "training__date")
    search_fields = (
        "technique__name",
        "training__user__username",
        "training__notes",
    )
    autocomplete_fields = ["training", "technique"]
    ordering = ("-training__date", "technique__name")