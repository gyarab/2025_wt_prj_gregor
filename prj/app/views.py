from django.shortcuts import render


def home(request):
    return render(request, "home.html")


def about(request):
    return render(request, "about.html")


def trainings(request):
    return render(request, "trainings.html")


def techniques(request):
    return render(request, "techniques.html")


def statistics(request):
    return render(request, "statistics.html")


def api_playground(request):
    return render(request, "api_playground.html")