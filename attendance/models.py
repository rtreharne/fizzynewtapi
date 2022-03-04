from django.db import models

from helpers.models import BaseModel

class Attendance(BaseModel):
    institute_fnid = models.CharField(max_length=128)
    school_fnid = models.CharField(max_length=128)
    course_fnid = models.CharField(max_length=128)
    session_fnid = models.CharField(max_length=128)
    student_fnid = models.CharField(max_length=128)
    session_type_fnid = models.CharField(max_length=128)
    group_fnid = models.CharField(max_length=128, blank=True, null=False, default=None)
    verified = models.BooleanField(default=False)
    present = models.BooleanField(default=False)
    late = models.BooleanField(default=False)
    session_code = models.CharField(max_length=128, blank=True, null=False, default=None)
    student_code = models.CharField(max_length=128)
    peer_code = models.CharField(max_length=128, blank=True, null=False, default=None)
    peer_verified = models.BooleanField(default=False)
    online = models.BooleanField(default=False)


    def __str__(self):
        return self.student_code

class Session(BaseModel):
    session_type_fnid = models.CharField(max_length=128)
    institute_fnid = models.CharField(max_length=128)
    school_fnid = models.CharField(max_length=128)
    course_fnid = models.CharField(max_length=128)
    average_attendance = models.DecimalField(default=0.0, max_digits=3, decimal_places=1)
    session_code = models.CharField(max_length=128)
    duration_hrs = models.DecimalField(default=1.0, max_digits=3, decimal_places=1)
    session_verification_required = models.BooleanField(default=False)
    peer_verification_required = models.BooleanField(default=False)
    late_hrs = models.DecimalField(default=12.0, max_digits=3, decimal_places=1)

    def __str__(self):
        return self.session_code

class SessionType(BaseModel):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=256, blank=True, null=False, default=None)

    def __str__(self):
        return self.name






