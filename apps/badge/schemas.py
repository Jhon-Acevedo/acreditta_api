from ninja import ModelSchema
from pydantic import EmailStr

from apps.badge.models import Badge
from ninja import Schema


class BadgeSchema(ModelSchema):
    class Meta:
        model = Badge
        fields = '__all__'


class BadgeCreateSchema(ModelSchema):
    class Meta:
        model = Badge
        exclude = ['id', 'path_image']


class AuthRequest(Schema):
    email: EmailStr
    password: str
