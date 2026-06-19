from django.shortcuts import render


def home(request):
    return render(request, "home.html")


def about(request):
    return render(request, "about.html")


def api_playground(request):
    return render(request, "api_playground.html")