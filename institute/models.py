from django.db import models
from helpers.models import TrackingModel
import uuid

class Institute(TrackingModel):
    fnid = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name
