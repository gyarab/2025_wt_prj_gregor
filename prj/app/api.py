from datetime import date, time
from typing import List, Optional

from django.contrib.auth.models import User
from django.db.models import Sum
from ninja import NinjaAPI, Schema

from .models import Technique, TechniqueStat, Training, TrainingResult

api = NinjaAPI(title="FightLog API")


class MessageSchema(Schema):
    message: str


class ResultIn(Schema):
    technique_id: int
    count: int = 1


class ResultOut(Schema):
    technique_id: int
    technique_name: str
    count: int


class TrainingIn(Schema):
    title: str
    date: date
    start_time: Optional[time] = None
    duration: int
    notes: str = ""
    draws: int = 0
    win_results: List[ResultIn] = []
    loss_results: List[ResultIn] = []


class TrainingOut(Schema):
    id: int
    title: str
    user_id: int
    username: str
    date: date
    start_time: Optional[time]
    duration: int
    notes: str
    wins: int
    losses: int
    draws: int
    win_results: List[ResultOut]
    loss_results: List[ResultOut]


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


class ChartItemOut(Schema):
    technique: str
    count: int


def get_default_user():
    user = User.objects.filter(username="admin").first()
    if user:
        return user

    user = User.objects.first()
    if user:
        return user

    return User.objects.create_user(username="admin", password="admin")


def result_to_dict(result):
    return {
        "technique_id": result.technique_id,
        "technique_name": result.technique.name,
        "count": result.count,
    }


def training_to_dict(training):
    win_results = [
        result_to_dict(result)
        for result in training.results.all()
        if result.result_type == TrainingResult.WIN
    ]

    loss_results = [
        result_to_dict(result)
        for result in training.results.all()
        if result.result_type == TrainingResult.LOSS
    ]

    return {
        "id": training.id,
        "title": training.title,
        "user_id": training.user_id,
        "username": training.user.username,
        "date": training.date,
        "start_time": training.start_time,
        "duration": training.duration,
        "notes": training.notes,
        "wins": training.wins,
        "losses": training.losses,
        "draws": training.draws,
        "win_results": win_results,
        "loss_results": loss_results,
    }


def save_results(training, result_type, results):
    for item in results:
        if item.count <= 0:
            continue

        technique = Technique.objects.get(id=item.technique_id)

        TrainingResult.objects.create(
            training=training,
            technique=technique,
            result_type=result_type,
            count=item.count,
        )


def update_training_counts(training):
    training.wins = (
        training.results
        .filter(result_type=TrainingResult.WIN)
        .aggregate(total=Sum("count"))["total"]
        or 0
    )

    training.losses = (
        training.results
        .filter(result_type=TrainingResult.LOSS)
        .aggregate(total=Sum("count"))["total"]
        or 0
    )

    training.save()


@api.get("/training", response=List[TrainingOut], tags=["training"])
def list_trainings(request):
    trainings = (
        Training.objects
        .select_related("user")
        .prefetch_related("results__technique")
        .all()
    )
    return [training_to_dict(training) for training in trainings]


@api.get(
    "/training/{training_id}",
    response={200: TrainingOut, 404: MessageSchema},
    tags=["training"],
)
def get_training(request, training_id: int):
    try:
        training = (
            Training.objects
            .select_related("user")
            .prefetch_related("results__technique")
            .get(id=training_id)
        )
    except Training.DoesNotExist:
        return 404, {"message": "Training not found"}

    return training_to_dict(training)


@api.post(
    "/training",
    response={201: TrainingOut, 400: MessageSchema, 404: MessageSchema},
    tags=["training"],
)
def create_training(request, payload: TrainingIn):
    try:
        user = get_default_user()

        training = Training.objects.create(
            user=user,
            title=payload.title,
            date=payload.date,
            start_time=payload.start_time,
            duration=payload.duration,
            notes=payload.notes,
            draws=payload.draws,
        )

        save_results(training, TrainingResult.WIN, payload.win_results)
        save_results(training, TrainingResult.LOSS, payload.loss_results)
        update_training_counts(training)

        training = (
            Training.objects
            .select_related("user")
            .prefetch_related("results__technique")
            .get(id=training.id)
        )

        return 201, training_to_dict(training)

    except Technique.DoesNotExist:
        return 404, {"message": "Technique not found"}

    except Exception as error:
        return 400, {"message": str(error)}


@api.put(
    "/training/{training_id}",
    response={200: TrainingOut, 400: MessageSchema, 404: MessageSchema},
    tags=["training"],
)
def update_training(request, training_id: int, payload: TrainingIn):
    try:
        training = Training.objects.get(id=training_id)

        training.title = payload.title
        training.date = payload.date
        training.start_time = payload.start_time
        training.duration = payload.duration
        training.notes = payload.notes
        training.draws = payload.draws
        training.save()

        training.results.all().delete()

        save_results(training, TrainingResult.WIN, payload.win_results)
        save_results(training, TrainingResult.LOSS, payload.loss_results)
        update_training_counts(training)

        training = (
            Training.objects
            .select_related("user")
            .prefetch_related("results__technique")
            .get(id=training.id)
        )

        return training_to_dict(training)

    except Training.DoesNotExist:
        return 404, {"message": "Training not found"}

    except Technique.DoesNotExist:
        return 404, {"message": "Technique not found"}

    except Exception as error:
        return 400, {"message": str(error)}


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
    name = payload.name.strip()

    technique, created = Technique.objects.get_or_create(name=name)

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
        Technique.objects.get(id=payload.technique_id)
    except Training.DoesNotExist:
        return 404, {"message": "Training not found"}
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


def chart_data(result_type):
    rows = (
        TrainingResult.objects
        .filter(result_type=result_type)
        .values("technique__name")
        .annotate(total=Sum("count"))
        .order_by("-total")
    )

    return [
        {
            "technique": row["technique__name"],
            "count": row["total"] or 0,
        }
        for row in rows
    ]


@api.get("/stats/wins", response=List[ChartItemOut], tags=["statistics"])
def win_statistics(request):
    return chart_data(TrainingResult.WIN)


@api.get("/stats/losses", response=List[ChartItemOut], tags=["statistics"])
def loss_statistics(request):
    return chart_data(TrainingResult.LOSS)

@api.delete(
    "/training/{training_id}",
    response={200: MessageSchema, 404: MessageSchema},
    tags=["training"],
)
def delete_training(request, training_id: int):
    try:
        training = Training.objects.get(id=training_id)
    except Training.DoesNotExist:
        return 404, {"message": "Training not found"}

    training.delete()
    return {"message": "Training deleted"}