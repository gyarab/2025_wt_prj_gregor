from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),

    path("api/training", views.training_create_api, name="training_create_api"),
    path("api/training/<int:training_id>", views.training_update_api, name="training_update_api"),
]