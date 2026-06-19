from django.contrib.auth.models import User
from django.db import models


class Training(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="trainings")
    date = models.DateField()
    start_time = models.TimeField(blank=True, null=True)
    duration = models.PositiveIntegerField(help_text="Délka tréninku v minutách")
    notes = models.TextField(blank=True)

    wins = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)
    draws = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-date", "-start_time"]
        verbose_name = "Training"
        verbose_name_plural = "Trainings"

    def __str__(self):
        return f"{self.user.username} - {self.date}"


class Technique(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Technique"
        verbose_name_plural = "Techniques"

    def __str__(self):
        return self.name


class TechniqueStat(models.Model):
    training = models.ForeignKey(
        Training,
        on_delete=models.CASCADE,
        related_name="technique_stats",
    )
    technique = models.ForeignKey(
        Technique,
        on_delete=models.CASCADE,
        related_name="technique_stats",
    )
    count = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["technique__name"]
        unique_together = ("training", "technique")
        verbose_name = "Technique stat"
        verbose_name_plural = "Technique stats"

    def __str__(self):
        return f"{self.training} - {self.technique.name} ({self.count})"