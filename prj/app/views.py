import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Training


def home(request):
    return JsonResponse({"message": "FightLog běží"})


def about(request):
    return JsonResponse({"message": "FightLog je tréninkový deník pro MMA a BJJ"})


@csrf_exempt
def training_create_api(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST method is allowed"}, status=405)

    try:
        data = json.loads(request.body)

        training = Training.objects.create(
            user_id=data["user"],
            date=data["date"],
            start_time=data.get("start_time"),
            duration=data["duration"],
            notes=data.get("notes", ""),
            wins=data.get("wins", 0),
            losses=data.get("losses", 0),
            draws=data.get("draws", 0),
        )

        return JsonResponse({
            "id": training.id,
            "message": "Training created successfully"
        }, status=201)

    except KeyError as error:
        return JsonResponse({"error": f"Missing field: {error}"}, status=400)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)


@csrf_exempt
def training_update_api(request, training_id):
    if request.method != "PUT":
        return JsonResponse({"error": "Only PUT method is allowed"}, status=405)

    try:
        training = Training.objects.get(id=training_id)
        data = json.loads(request.body)

        training.date = data.get("date", training.date)
        training.start_time = data.get("start_time", training.start_time)
        training.duration = data.get("duration", training.duration)
        training.notes = data.get("notes", training.notes)
        training.wins = data.get("wins", training.wins)
        training.losses = data.get("losses", training.losses)
        training.draws = data.get("draws", training.draws)

        training.save()

        return JsonResponse({
            "id": training.id,
            "message": "Training updated successfully"
        })

    except Training.DoesNotExist:
        return JsonResponse({"error": "Training not found"}, status=404)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)