from django.utils import timezone
from attendance.models import Attendance, Session

def calculate_attendance(queryset):
    """
    Calculates the attendance percentage of a student
    :param attendance: A list of attendance records
    :return: The attendance 
    
    Ignore sessions that have been 
      + cancelled 
      + voided 
      + are in the future 
      + do not have approved absence
    """
    try:
        present = queryset.filter(present=True).count()
        total = queryset.count()

        average_attendance = float('{0:5g}'.format(present / total * 100))
    except ZeroDivisionError:
        average_attendance = 0
    return average_attendance