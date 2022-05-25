from django.db import models
from helpers.models import BaseModel
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime
from django.utils import timezone


class Course(BaseModel):

    institute_fnid = models.CharField(max_length=128)
    code = models.CharField(max_length=9, help_text="(e.g. MATH101)")
    name = models.CharField(max_length=128)
    visible = models.BooleanField(default=True)




    class Meta:
        unique_together = ('institute_fnid', 'code',)

    def __str__(self):
        return self.name


class CourseStudent(BaseModel):

    institute_fnid = models.CharField(max_length=128)
    course_fnid = models.CharField(max_length=128)
    student_fnid = models.CharField(max_length=128)
    course_instance_fnid = models.CharField(max_length=128, default="")

    class Meta:
        unique_together = ('course_fnid', 'student_fnid')

    def __str__(self):
        return self.student_fnid

class CourseInstance(BaseModel):

    institute_fnid = models.CharField(max_length=128)
    course_fnid = models.CharField(max_length=128)
    term_fnid = models.CharField(max_length=128)
    threshold = models.IntegerField(default=10, validators=[MaxValueValidator(100), MinValueValidator(1)])
    start_date_override = models.DateField(null=True, blank=True)
    end_date_override = models.DateField(null=True, blank=True)
    registration_start_override = models.DateField(null=True, blank=True)

    repeat = models.BooleanField(default=True)
    visible = models.BooleanField(default=True)

    def __str__(self):
        return self.course_fnid




