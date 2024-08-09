from ninja import ModelSchema
from apps.badge.models import Badge


class BadgeSchema(ModelSchema):
    class Meta:
        model = Badge
        fields = '__all__'


class BadgeCreateSchema(ModelSchema):
    class Meta:
        model = Badge
        exclude = ['id', 'path_image']
