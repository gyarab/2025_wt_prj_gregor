from django.shortcuts import render


def render_home(request):
    return render(request, "home.html")


def render_about(request):
    return render(request, "about.html")


def render_api_playground(request):
    return render(request, "api_playground.html")