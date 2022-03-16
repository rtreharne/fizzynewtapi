import django
django.setup()

print("Hello Rob")

from institute.models import *
from student.models import *
from programme.models import *
from course.models import *
from school.models import *

Institute.objects.all().delete()
InstituteDomain.objects.all().delete()
InstituteConfig.objects.all().delete()
Programme.objects.all().delete()
Course.objects.all().delete()
CourseStudent.objects.all().delete()
School.objects.all().delete()
Student.objects.all().delete()
StudentEmail.objects.all().delete()

print("database is clean")
