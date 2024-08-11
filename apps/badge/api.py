from botocore.exceptions import ClientError
from django.contrib.auth.models import User
from ninja import NinjaAPI, UploadedFile
from ninja.errors import HttpError
from rest_framework.generics import get_object_or_404

from apps.badge.auth import CognitoAuth
from apps.badge.models import Badge
from apps.badge.schemas import BadgeSchema, BadgeCreateSchema, AuthRequest, UserCreateSchema

app = NinjaAPI(
    version="1.0.0",
    urls_namespace="api",
    title="API Insignias",
    description="Create by Jhon-Acevedo",
    auth=CognitoAuth()
)


@app.post("/login", tags=["Auth"], auth=None)
def authenticate_user(request, data: AuthRequest):
    try:
        token = CognitoAuth.get_token_user(data.email, data.password)
        return token
    except ClientError as e:
        raise HttpError(401, f"Authentication Error: {str(e)}")


@app.get("/badge", response=list[BadgeSchema], tags=["Badge"], auth=CognitoAuth())
def list_badges(request):
    return Badge.objects.all()


@app.get("/badge/{badge_id}", response=BadgeSchema, tags=["Badge"], auth=None)
def get_badge(request, badge_id):
    badge = get_object_or_404(Badge, id=badge_id)
    return badge


@app.post("/badge", response=BadgeSchema, tags=["Badge"], auth=CognitoAuth())
def create_badge(request, badge: BadgeCreateSchema, image: UploadedFile = None):
    username = request.auth.get('username')
    user = get_object_or_404(User, username=username)
    badge = Badge.objects.create(
        name=badge.name,
        description=badge.description,
        id_user=user,
    )
    if image:
        badge.path_image.save(image.name, image)
    return badge


@app.post("/create_user", tags=["Auth"], auth=None)
def create_user(request, data: UserCreateSchema):
    try:
        user = CognitoAuth.create_user(data.email, data.password, data.name)
        return user
    except HttpError as e:
        raise HttpError(400, f"User creation error: {str(e)}")
