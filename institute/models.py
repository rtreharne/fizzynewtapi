from django.db import models
from helpers.models import TrackingModel
import uuid
from django.core.validators import URLValidator

class Institute(TrackingModel):
    fnid = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class InstituteDomain(TrackingModel):
    fnid = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4, editable=False)
    institute_fnid = models.CharField(max_length=128)
    domain = models.CharField(max_length=128, validators=[URLValidator])
    primary = models.BooleanField(default=False)

    class Meta:
        unique_together = ('institute_fnid', 'domain',)

    def __str__(self):
        self.domain