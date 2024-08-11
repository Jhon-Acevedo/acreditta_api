from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path

from apps.badge.api import app


def redirect_to_api(request):
    return HttpResponseRedirect('/api/docs')


urlpatterns = [
    # path('admin/', admin.site.urls),
    path("api/", app.urls),
    path("", redirect_to_api),
]
