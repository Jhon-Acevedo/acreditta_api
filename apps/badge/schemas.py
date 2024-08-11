from ninja import ModelSchema
from pydantic import EmailStr, BaseModel

from apps.badge.models import Badge
from ninja import Schema


class BadgeSchema(ModelSchema):
    class Meta:
        model = Badge
        fields = '__all__'


class BadgeCreateSchema(ModelSchema):
    class Meta:
        model = Badge
        exclude = ['id', 'path_image', 'id_user']


class AuthRequest(Schema):
    email: EmailStr
    password: str


class UserCreateSchema(BaseModel):
    email: EmailStr
    password: str
    name: str
