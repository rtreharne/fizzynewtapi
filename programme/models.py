from django.db import models
from helpers.models import BaseModel


class Programme(BaseModel):

    institute_fnid = models.CharField(max_length=128)
    school_fnid = models.CharField(max_length=128)
    name = models.CharField(max_length=128)

    class Meta:
        unique_together = ('school_fnid', 'name',)

    def __str__(self):
        return self.name

