import uuid
from django.contrib.auth.models import User
from django.db import models


class Badge(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    path_image = models.ImageField(upload_to='', null=True, blank=True)
    create_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
