from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("trainings/", views.trainings, name="trainings"),
    path("techniques/", views.techniques, name="techniques"),
    path("statistics/", views.statistics, name="statistics"),
    path("api_playground/", views.api_playground, name="api_playground"),
]