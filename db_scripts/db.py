import django
django.setup()

from school.models import School
from institute.models import Institute
from programme.models import Programme
from course.models import CourseIntake, Course, CourseStudent
from student.models import Student
import datetime
import random
import names

# get the test institute
institute = Institute.objects.get(name="Rob's University")

# clean
School.objects.filter(institute_fnid=institute.fnid).delete()
Programme.objects.filter(institute_fnid=institute.fnid).delete()
Course.objects.filter(institute_fnid=institute.fnid).delete()
Course.objects.filter(institute_fnid=institute.fnid).delete()
Student.objects.filter(institute_fnid=institute.fnid).delete()
CourseIntake.objects.filter(institute_fnid=institute.fnid).delete()
CourseStudent.objects.filter(institute_fnid=institute.fnid).delete()


def create_school(name, institute):
    school = School(name=name, institute_fnid=institute.fnid)
    school.save()
    return school

def create_programme(name, school, institute):
    programme = Programme(name=name, school_fnid=school.fnid, institute_fnid=institute.fnid)
    programme.save()
    return programme

def create_course(name, institute):
    course = Course(code=name, name=name, institute_fnid=institute.fnid)
    course.save()
    return course

def create_course_intake(course, institute, start, duration):
    course_intake = CourseIntake(
        course_fnid=course.fnid,
        institute_fnid=institute.fnid,
        start=datetime.datetime.strptime(start, "%Y-%m-%d"),
        duration_weeks=duration
    )
    course_intake.save()
    return course_intake

def create_student(last_name, first_name, institute, programme, year, student_id):
    student = Student(
        last_name=last_name,
        first_name=first_name,
        institute_fnid=institute.fnid,
        programme_fnid=programme.fnid,
        school_fnid=programme.school_fnid,
        year_of_study=year,
        student_id=student_id,
        verified=True
    )
    if random.uniform(0, 1) < 0.1:
        student.international = True

    student.save()

    return student


def create_enrollment(intake, student, institute):
    enrollment = CourseStudent(
        student_fnid=student.fnid,
        course_fnid=intake.course_fnid,
        institute_fnid=institute.fnid,
        intake_fnid=intake.fnid)

    enrollment.save()
    return enrollment


# create schools
print("creating schools ...")
schools = [
   create_school("School {}".format(i+1), institute) for i in range(4)
]

# create programmes
print("creating programmes ...")
programmes = [
    create_programme("Programme {0} ({1})".format(i+1, school.name), school, institute) for i in range(4) for school in schools
]

# create courses
print("creating courses ...")
course_names = ["CRSE{0}".format(str((i+1)*100 + j)) for i in range(4) for j in range(1, 40)]
courses = [
    create_course(name, institute) for name in course_names
]

# create intakes
print("creating intakes ...")
intakes = []
for course in courses:
    if random.uniform(0, 1) < 0.2:
        intakes.append(create_course_intake(course, institute, "2021-09-01", 15))
        intakes.append(create_course_intake(course, institute, "2022-02-01", 15))
    else:
        intakes.append(create_course_intake(course, institute, "2021-09-01", 52))

# create students
print("creating students ...")
student_names = list(set([names.get_full_name() for x in range(0, 2000)]))

s = []
student_id = 100000001
for programme in programmes:
    students = random.sample(student_names, random.randrange(50, 120))
    for student in students:
        last_name = student.split(" ")[-1]
        first_name = student.split(" ")[0]
        s.append(create_student(last_name, first_name, institute, programme, random.randrange(1,5), student_id))
        student_id += 1

# create enrollments
print("creating enrollments")
for intake in intakes:
    course = Course.objects.get(fnid=intake.course_fnid)
    course_year = int(course.name[4])
    students_year = [x for x in s if x.year_of_study == course_year]
    intake_list = random.choices(students_year, k=random.randrange(10, 30))
    for student in intake_list:
        create_enrollment(intake, student, institute)




