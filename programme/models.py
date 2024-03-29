from django.db import models
from helpers.models import BaseModel
from django.core.validators import MinValueValidator, MaxValueValidator


class Programme(BaseModel):

    institute_fnid = models.UUIDField()
    school_fnid = models.UUIDField()
    code = models.CharField(max_length=9, blank=None, null=True)
    name = models.CharField(max_length=128)
    term_start_week = models.PositiveIntegerField(default=34, validators=[MinValueValidator(1), MaxValueValidator(52)])
    active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('school_fnid', 'name')

    def __str__(self):
        return self.name

