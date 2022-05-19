from django.db import models
import uuid
import datetime



class TrackingModel(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True
        ordering=('-created_at',)

class BaseModel(models.Model):
    fnid = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4, editable=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True
        ordering=('-created_at',)

"""
def get_start_date_from_week(fnid):
    institute_config = InstituteConfig.objects.get(institute_fnid=fnid)
    year = datetime.datetime.now.year()
    week = institute_config.term_start_week
    d = "{}-W{}".format(str(year), str(week))
    date = datetime.datetime.strptime(d + '-1', "%Y-W%W-%w")
    return date

"""