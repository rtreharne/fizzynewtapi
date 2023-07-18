from django.db import models
from helpers.models import BaseModel
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime
from django.utils import timezone


class Course(BaseModel):

    institute_fnid = models.UUIDField()
    code = models.CharField(max_length=9, help_text="(e.g. MATH101)")
    name = models.CharField(max_length=128)
    visible = models.BooleanField(default=True)

    class Meta:
        unique_together = ('institute_fnid', 'code',)

    def __str__(self):
        return self.name


class CourseInstanceStudent(BaseModel):

    institute_fnid = models.UUIDField()
    student_fnid = models.UUIDField()
    course_instance_fnid = models.UUIDField(null=True, blank=True)
    average_attend_pc = models.DecimalField(default=0.0, decimal_places=1, max_digits=4)
    resit = models.BooleanField(default=False)

    class Meta:
        unique_together = ('institute_fnid', 'course_instance_fnid', 'student_fnid')

    def __str__(self):
        return self.student_fnid

class CourseInstance(BaseModel):

    institute_fnid = models.UUIDField()
    course_fnid = models.UUIDField()
    term_fnid = models.UUIDField()
    name_override = models.CharField(max_length=128)
    threshold_override = models.IntegerField(null=True, blank=True, validators=[MaxValueValidator(100), MinValueValidator(1)])
    start_date_override = models.DateField(null=True, blank=True)
    end_date_override = models.DateField(null=True, blank=True)
    registration_start_override = models.DateField(null=True, blank=True)
    last_session = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=True)
    repeat = models.BooleanField(default=True)
    visible = models.BooleanField(default=True)

    class Meta:
        unique_together = ('term_fnid', 'name_override')

    def __str__(self):
        return self.course_fnid
    
class Group(BaseModel):

    institute_fnid = models.UUIDField()
    course_instance_fnid = models.UUIDField()
    name = models.CharField(max_length=128)


    class Meta:
        unique_together = ('course_instance_fnid', 'name')

    def __str__(self):
        return self.name
    
class GroupStudent(BaseModel):

    institute_fnid = models.UUIDField()
    group_fnid = models.UUIDField()
    student_fnid = models.UUIDField()

    class Meta:
        unique_together = ('group_fnid', 'student_fnid')

    def __str__(self):
        return self.group_fnid






