from datetime import date, time
from typing import List, Optional

from django.contrib.auth.models import User
from ninja import NinjaAPI, Schema

from .models import Technique, TechniqueStat, Training

api = NinjaAPI(title="FightLog API")


class MessageSchema(Schema):
    message: str


class TrainingIn(Schema):
    user_id: int
    date: date
    start_time: Optional[time] = None
    duration: int
    notes: str = ""
    wins: int = 0
    losses: int = 0
    draws: int = 0


class TrainingOut(Schema):
    id: int
    user_id: int
    username: str
    date: date
    start_time: Optional[time]
    duration: int
    notes: str
    wins: int
    losses: int
    draws: int


class TechniqueIn(Schema):
    name: str


class TechniqueOut(Schema):
    id: int
    name: str


class TechniqueStatIn(Schema):
    training_id: int
    technique_id: int
    count: int = 1


class TechniqueStatOut(Schema):
    id: int
    training_id: int
    technique_id: int
    technique_name: str
    count: int


def training_to_dict(training: Training):
    return {
        "id": training.id,
        "user_id": training.user_id,
        "username": training.user.username,
        "date": training.date,
        "start_time": training.start_time,
        "duration": training.duration,
        "notes": training.notes,
        "wins": training.wins,
        "losses": training.losses,
        "draws": training.draws,
    }


@api.get("/training", response=List[TrainingOut], tags=["training"])
def list_trainings(request):
    trainings = Training.objects.select_related("user").all()
    return [training_to_dict(training) for training in trainings]


@api.get(
    "/training/{training_id}",
    response={200: TrainingOut, 404: MessageSchema},
    tags=["training"],
)
def get_training(request, training_id: int):
    try:
        training = Training.objects.select_related("user").get(id=training_id)
    except Training.DoesNotExist:
        return 404, {"message": "Training not found"}

    return training_to_dict(training)


@api.post(
    "/training",
    response={201: TrainingOut, 404: MessageSchema},
    tags=["training"],
)
def create_training(request, payload: TrainingIn):
    try:
        User.objects.get(id=payload.user_id)
    except User.DoesNotExist:
        return 404, {"message": "User not found"}

    training = Training.objects.create(**payload.dict())
    training = Training.objects.select_related("user").get(id=training.id)

    return 201, training_to_dict(training)


@api.put(
    "/training/{training_id}",
    response={200: TrainingOut, 404: MessageSchema},
    tags=["training"],
)
def update_training(request, training_id: int, payload: TrainingIn):
    try:
        training = Training.objects.select_related("user").get(id=training_id)
    except Training.DoesNotExist:
        return 404, {"message": "Training not found"}

    try:
        User.objects.get(id=payload.user_id)
    except User.DoesNotExist:
        return 404, {"message": "User not found"}

    for key, value in payload.dict().items():
        setattr(training, key, value)

    training.save()
    training = Training.objects.select_related("user").get(id=training.id)

    return training_to_dict(training)


@api.get("/technique", response=List[TechniqueOut], tags=["technique"])
def list_techniques(request):
    return Technique.objects.all()


@api.get(
    "/technique/{technique_id}",
    response={200: TechniqueOut, 404: MessageSchema},
    tags=["technique"],
)
def get_technique(request, technique_id: int):
    try:
        return Technique.objects.get(id=technique_id)
    except Technique.DoesNotExist:
        return 404, {"message": "Technique not found"}


@api.post("/technique", response={201: TechniqueOut}, tags=["technique"])
def create_technique(request, payload: TechniqueIn):
    technique = Technique.objects.create(name=payload.name)
    return 201, technique


@api.get("/technique-stat", response=List[TechniqueStatOut], tags=["technique-stat"])
def list_technique_stats(request):
    stats = TechniqueStat.objects.select_related("training", "technique").all()

    return [
        {
            "id": stat.id,
            "training_id": stat.training_id,
            "technique_id": stat.technique_id,
            "technique_name": stat.technique.name,
            "count": stat.count,
        }
        for stat in stats
    ]


@api.post(
    "/technique-stat",
    response={201: TechniqueStatOut, 404: MessageSchema},
    tags=["technique-stat"],
)
def create_technique_stat(request, payload: TechniqueStatIn):
    try:
        Training.objects.get(id=payload.training_id)
    except Training.DoesNotExist:
        return 404, {"message": "Training not found"}

    try:
        Technique.objects.get(id=payload.technique_id)
    except Technique.DoesNotExist:
        return 404, {"message": "Technique not found"}

    stat = TechniqueStat.objects.create(**payload.dict())
    stat = TechniqueStat.objects.select_related("technique").get(id=stat.id)

    return 201, {
        "id": stat.id,
        "training_id": stat.training_id,
        "technique_id": stat.technique_id,
        "technique_name": stat.technique.name,
        "count": stat.count,
    }