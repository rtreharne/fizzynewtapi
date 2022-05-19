import django
django.setup()

from student.models import Student, StudentEmail
from course.models import CourseStudent

# Delete students
Student.objects.all().delete()
StudentEmail.objects.all().delete()
print("Students have been cleaned.")


# Delete enrollments
CourseStudent.objects.all().delete()
print("Student enrollments have been cleaned.")