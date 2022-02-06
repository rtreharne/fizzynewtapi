from django.db import models
from helpers.models import BaseModel


class Course(BaseModel):

    institute_fnid = models.CharField(max_length=128)
    code = models.CharField(max_length=9, help_text="(e.g. MATH101)")
    name = models.CharField(max_length=128)
    visible = models.BooleanField(default=True)

    class Meta:
        unique_together = ('institute_fnid', 'code',)


    def __str__(self):
        return self.name

