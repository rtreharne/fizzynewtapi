from django.db import models
from helpers.models import BaseModel
from django.core.validators import MinValueValidator, MaxValueValidator


class Programme(BaseModel):

    institute_fnid = models.CharField(max_length=128)
    school_fnid = models.CharField(max_length=128)
    code = models.CharField(max_length=9, blank=None, null=True)
    name = models.CharField(max_length=128)
    term_start_week = models.PositiveIntegerField(default=34, validators=[MinValueValidator(1), MaxValueValidator(52)])

    class Meta:
        unique_together = ('school_fnid', 'name')

    def __str__(self):
        return self.name

