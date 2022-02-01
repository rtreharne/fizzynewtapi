from django.db import models
from helpers.models import TrackingModel
import uuid


class Todo(TrackingModel):
    fnid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)

    def __str__(self):
        self.name


