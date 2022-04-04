import django
django.setup()

from attendance.models import Session, Attendance

# Delete sessions
Session.objects.all().delete()
print("Sessions have been cleaned.")


# Delete attendance logs
Attendance.objects.all().delete()
print("Attendance logs have been cleaned.")