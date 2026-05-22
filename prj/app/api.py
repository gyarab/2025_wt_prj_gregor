from typing import List

from django.shortcuts import get_object_or_404
from ninja import NinjaAPI, Schema

from .models import Training


api = NinjaAPI(title="FightLog API")


class MessageSchema(Schema):
    message: str


class TrainingOut(Schema):
    id: int
    date: str
    start_time: str = None
    duration: int
    notes: str
    wins: int
    losses: int
    draws: int


class TrainingIn(Schema):
    user_id: int
    date: str
    start_time: str = None
    duration: int
    notes: str = ""
    wins: int = 0
    losses: int = 0
    draws: int = 0


@api.get("/training", response=List[TrainingOut], tags=["training"])
def list_trainings(request):
    trainings = Training.objects.all()

    return [
        {
            "id": training.id,
            "date": str(training.date),
            "start_time": str(training.start_time) if training.start_time else None,
            "duration": training.duration,
            "notes": training.notes,
            "wins": training.wins,
            "losses": training.losses,
            "draws": training.draws,
        }
        for training in trainings
    ]


@api.get("/training/{training_id}", response={200: TrainingOut, 404: MessageSchema}, tags=["training"])
def get_training(request, training_id: int):
    training = get_object_or_404(Training, id=training_id)

    return {
        "id": training.id,
        "date": str(training.date),
        "start_time": str(training.start_time) if training.start_time else None,
        "duration": training.duration,
        "notes": training.notes,
        "wins": training.wins,
        "losses": training.losses,
        "draws": training.draws,
    }


@api.post("/training", response={201: TrainingOut}, tags=["training"])
def create_training(request, payload: TrainingIn):
    training = Training.objects.create(
        user_id=payload.user_id,
        date=payload.date,
        start_time=payload.start_time,
        duration=payload.duration,
        notes=payload.notes,
        wins=payload.wins,
        losses=payload.losses,
        draws=payload.draws,
    )

    return 201, {
        "id": training.id,
        "date": str(training.date),
        "start_time": str(training.start_time) if training.start_time else None,
        "duration": training.duration,
        "notes": training.notes,
        "wins": training.wins,
        "losses": training.losses,
        "draws": training.draws,
    }


@api.put("/training/{training_id}", response={200: TrainingOut, 404: MessageSchema}, tags=["training"])
def update_training(request, training_id: int, payload: TrainingIn):
    training = get_object_or_404(Training, id=training_id)

    training.user_id = payload.user_id
    training.date = payload.date
    training.start_time = payload.start_time
    training.duration = payload.duration
    training.notes = payload.notes
    training.wins = payload.wins
    training.losses = payload.losses
    training.draws = payload.draws
    training.save()

    return {
        "id": training.id,
        "date": str(training.date),
        "start_time": str(training.start_time) if training.start_time else None,
        "duration": training.duration,
        "notes": training.notes,
        "wins": training.wins,
        "losses": training.losses,
        "draws": training.draws,
    }