from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from ninja import NinjaAPI
from ninja.files import UploadedFile

from apps.badge.models import Badge
from apps.badge.schemas import BadgeSchema, BadgeCreateSchema

app = NinjaAPI(version="1.0.0", urls_namespace="badge", title="Insignia API", description="Create by Jhon-Acevedo ("
                                                                                       "jhonedwin.acevedo1@gmail.com)")


@app.get("/badge", response=list[BadgeSchema], tags=["Badge"])
def list_badges(request):
    return Badge.objects.all()


@app.get("/badge/{badge_id}", response=BadgeSchema, tags=["Badge"])
def get_badge(request, badge_id):
    badge = get_object_or_404(Badge, id=badge_id)
    return badge


@app.post("/badge", response=BadgeSchema, tags=["Badge"])
def create_badge(request, badge: BadgeCreateSchema, image: UploadedFile = None):
    user = get_object_or_404(User, id=badge.create_by)
    badge = Badge.objects.create(
        name=badge.name,
        description=badge.description,
        create_by=user,
    )
    if image:
        badge.path_image.save(image.name, image)
    return badge
