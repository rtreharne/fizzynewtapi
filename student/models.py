from django.db import models
from helpers.models import BaseModel


class Student(BaseModel):

    study_year = ((1, '1'),
                  (2, '2'),
                  (3, '3'),
                  (4, '4'),
                  (5, '5'),
                  (6, '6'),
                  (7, '7'))

    institute_fnid = models.CharField(max_length=128)
    school_fnid = models.CharField(max_length=128, null=True, blank=True)
    programme_fnid = models.CharField(max_length=128, null=True, blank=True)
    year_of_study = models.IntegerField(choices=study_year, null=True, blank=True)
    student_id = models.CharField(max_length=12, unique=True, null=True, blank=True, default=None)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    international = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)


    class Meta:
        unique_together = ('institute_fnid', 'student_id',)

    def __str__(self):
        return self.name

class StudentEmail(BaseModel):
    institute_fnid = models.CharField(max_length=128)
    student_fnid = models.CharField(max_length=128)
    email = models.EmailField(max_length=128, unique=True)
    primary = models.BooleanField(default=False)

    def __str__(self):
        return self.email



