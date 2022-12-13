from django.db import models

from helpers.models import BaseModel


class Attendance(BaseModel):
    institute_fnid = models.CharField(max_length=128)
    school_fnid = models.CharField(max_length=128)
    course_instance_fnid = models.CharField(max_length=128)
    session_fnid = models.CharField(max_length=128)
    student_fnid = models.CharField(max_length=128)
    session_type_fnid = models.CharField(max_length=128)
    group_fnid = models.CharField(max_length=128, blank=True, null=True, default=None)
    verified = models.BooleanField(default=False)
    present = models.BooleanField(default=False)
    late = models.BooleanField(default=False)

    def __str__(self):
        return str(self.fnid)


class Session(BaseModel):
    session_type_fnid = models.CharField(max_length=128)
    institute_fnid = models.CharField(max_length=128)
    course_instance_fnid = models.CharField(max_length=128)
    session_start = models.DateTimeField()
    duration_mins = models.IntegerField(default=60)
    session_audit = models.BooleanField(default=False)
    ignore = models.BooleanField(default=False)
    attendance = models.DecimalField(default=0.0, max_digits=4, decimal_places=1)
    online = models.BooleanField(default=False)

    def __str__(self):
        return str(self.fnid)


class SessionRequest(BaseModel):
    institute_fnid = models.CharField(max_length=128)
    student_fnid = models.CharField(max_length=128)
    course_instance_fnid = models.CharField(max_length=128)
    session_start = models.DateTimeField()
    session_type_fnid = models.CharField(max_length=128)
    duration_mins = models.IntegerField(default=60)
    online = models.BooleanField(default=False)
    session_fnid = models.CharField(max_length=128, default=None, null=True)


    def __str__(self):
        return str(self.fnid)






