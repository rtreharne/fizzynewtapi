from django.db import models

from helpers.models import BaseModel


class Attendance(BaseModel):
    institute_fnid = models.UUIDField()
    school_fnid = models.UUIDField()
    programme_fnid = models.UUIDField(blank=True, null=True)
    course_instance_fnid = models.UUIDField()
    session_fnid = models.UUIDField()
    student_fnid = models.UUIDField()
    session_type_fnid = models.UUIDField()
    group_fnid = models.UUIDField(blank=True, null=True)
    verified = models.BooleanField(default=False)
    present = models.BooleanField(default=False)
    late = models.BooleanField(default=False)
    void = models.BooleanField(default=False)
    verified_by_administrator = models.CharField(max_length=128, null=True, default=None)
    verified_by_audit = models.CharField(max_length=128, null=True, default=None)
    approved_absence = models.BooleanField(default=False)

    def __str__(self):
        return str(self.fnid)


class Session(BaseModel):
    session_type_fnid = models.UUIDField()
    institute_fnid = models.UUIDField()
    course_instance_fnid = models.UUIDField()
    group_fnid = models.UUIDField(blank=True, null=True)
    session_start = models.DateTimeField()
    duration_mins = models.IntegerField(default=60)
    session_audit = models.BooleanField(default=False)
    ignore = models.BooleanField(default=False)
    attendance = models.DecimalField(default=0.0, max_digits=4, decimal_places=1)
    online = models.BooleanField(default=False)
    expired = models.BooleanField(default=False)
    cancelled_by = models.CharField(max_length=128, null=True, default=None)
    cancelled = models.BooleanField(default=False)
    mandatory = models.BooleanField(default=True)
    void = models.BooleanField(default=False)

    def __str__(self):
        return str(self.fnid)


class SessionRequest(BaseModel):
    institute_fnid = models.UUIDField()
    student_fnid = models.UUIDField()
    group_fnid = models.UUIDField(blank=True, null=True)
    course_instance_fnid = models.UUIDField()
    session_start = models.DateTimeField()
    session_type_fnid = models.UUIDField()
    duration_mins = models.IntegerField(default=60)
    online = models.BooleanField(default=False)
    session_fnid = models.UUIDField(max_length=128, null=True)
    expired = models.BooleanField(default=False)


    def __str__(self):
        return str(self.fnid)






