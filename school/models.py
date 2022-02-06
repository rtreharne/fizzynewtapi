from django.db import models
from helpers.models import BaseModel


class School(BaseModel):

    institute_fnid = models.CharField(max_length=128)
    name = models.CharField(max_length=128)

    class Meta:
        unique_together = ('institute_fnid', 'name',)

    def __str__(self):
        return self.name

