from django.db import models
from helpers.models import TrackingModel, BaseModel
import uuid
from django.core.validators import URLValidator, MaxValueValidator, MinValueValidator

class Institute(TrackingModel):
    fnid = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name


class InstituteDomain(TrackingModel):
    fnid = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4, editable=False)
    institute_fnid = models.CharField(max_length=128)
    domain = models.CharField(max_length=128, validators=[URLValidator], unique=True)
    primary = models.BooleanField(default=False)
    tenant = models.CharField(max_length=256, unique=True, blank=True, null=True)
    admin_consent = models.BooleanField(default=False)

    class Meta:
        unique_together = ('institute_fnid', 'domain',)

    def __str__(self):
        self.domain


class InstituteConfig(BaseModel):
    institute_fnid = models.UUIDField()
    student_id_required = models.BooleanField(default=False)
    term_start_week = models.PositiveIntegerField(default=35, validators=[MinValueValidator(1), MaxValueValidator(52)])

    def __str__(self):
        self.institute_fnid

class Term(BaseModel):
    institute_fnid = models.UUIDField()
    label = models.CharField(max_length=128)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)
    registration_start = models.DateTimeField()
    active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('institute_fnid', 'label')

    def __str__(self):
        return self.label


class Year(BaseModel):
    institute_fnid = models.UUIDField()
    label = models.CharField(max_length=128)
    previous_year_fnid = models.UUIDField(blank=True, null=True)
    next_year_fnid = models.UUIDField(blank=True, null=True)

    class Meta:
        unique_together = ('institute_fnid', 'label',)

    def __str__(self):
        return self.label


class SessionType(BaseModel):
    institute_fnid = models.UUIDField()
    label = models.CharField(max_length=128)

    class Meta:
        unique_together = ('institute_fnid', 'label')

    def __str__(self):
        return self.label

