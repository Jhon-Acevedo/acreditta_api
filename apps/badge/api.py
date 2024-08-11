import boto3
from botocore.exceptions import ClientError
from django.contrib.auth.models import User
from django.forms import Form
from ninja import NinjaAPI, UploadedFile
from ninja.errors import HttpError
from ninja.security import HttpBearer
from pydantic_core import ValidationError
from rest_framework.generics import get_object_or_404

from acreditta_api import settings
from apps.badge.auth import CognitoAuth
from apps.badge.models import Badge
from apps.badge.schemas import BadgeSchema, BadgeCreateSchema, AuthRequest

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
        data = AuthRequest(**data.dict())
        client = boto3.client('cognito-idp', region_name=settings.COGNITO_REGION)
        response = client.initiate_auth(
            ClientId=settings.COGNITO_CLIENT_ID,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': data.email,
                'PASSWORD': data.password,
            }
        )
        return {
            'access_token': response['AuthenticationResult']['AccessToken'],
            'refresh_token': response['AuthenticationResult']['RefreshToken'],
        }
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
    user = get_object_or_404(User, id=badge.create_by)
    badge = Badge.objects.create(
        name=badge.name,
        description=badge.description,
        create_by=user,
    )
    if image:
        badge.path_image.save(image.name, image)
    return badge
