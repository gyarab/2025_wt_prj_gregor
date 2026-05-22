from django.contrib import admin
from django.urls import path
from app import views
from app.api import api

urlpatterns = [
    path("api/", api.urls),
    path("admin/", admin.site.urls),
    path("", views.render_home, name="home"),
    path("about/", views.render_about, name="about"),
    path("api_playground/", views.render_api_playground, name="api_playground"),
]