from ninja import NinjaAPI

from apps.badge.models import Badge
from apps.badge.schemas import BadgeSchema

app = NinjaAPI()


@app.get("/badge", response=list[BadgeSchema])
def list_badges(request):
    return Badge.objects.all()
