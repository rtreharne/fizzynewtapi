from django.db import models
from helpers.models import BaseModel

class Student(BaseModel):

    study_year = ((0, '0'),
                  (1, '1'),
                  (2, '2'),
                  (3, '3'),
                  (4, '4'),
                  (5, '5'),
                  (6, '6'),
                  (7, '7'))

    institute_fnid = models.UUIDField()
    school_fnid = models.UUIDField(blank=True, null=True)
    programme_fnid = models.UUIDField(blank=True, null=True)
    year_of_study = models.IntegerField()
    student_id = models.CharField(max_length=20, null=True, blank=True, default=None)
    first_name = models.CharField(max_length=128, null=True, blank=True)
    last_name = models.CharField(max_length=128, null=True, blank=True)
    undergraduate = models.BooleanField(default=True)
    international = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    average_attend_pc = models.DecimalField(default=0.0, decimal_places=1, max_digits=5)
    active = models.BooleanField(default=True)


    class Meta:
        unique_together = ('institute_fnid', 'student_id',)

    def __str__(self):
        return self.last_name

class StudentEmail(BaseModel):
    institute_fnid = models.UUIDField()
    student_fnid = models.UUIDField()
    email = models.EmailField(max_length=128, unique=True)
    primary = models.BooleanField(default=False)

    def __str__(self):
        return self.email

class StudentTerm(BaseModel):
    institute_fnid = models.UUIDField()
    student_fnid = models.UUIDField()
    term_fnid = models.UUIDField()
    current = models.BooleanField(default=True)





