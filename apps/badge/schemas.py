from ninja import ModelSchema

from apps.badge.models import Badge


class BadgeSchema(ModelSchema):
    class Meta:
        model = Badge
        fields = '__all__'
