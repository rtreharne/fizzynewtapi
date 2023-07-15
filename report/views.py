from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from student.models import Student
from course.models import Course, CourseInstanceStudent, CourseInstance
from attendance.models import SessionRequest
from institute.models import Institute
from school.models import School
from programme.models import Programme
from attendance.models import Session, Attendance
from datetime import datetime, timedelta
from rest_framework.permissions import IsAuthenticated
from attendance.serializers import SessionRequestSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from helpers.token_params import *
import helpers.filters


def get_or_false(classmodel, parameter):
    if parameter:
        try:
            classmodel.objects.get(fnid=parameter)
            return True
        except classmodel.DoesNotExist:
            return False
    else:
        return True


class ActiveSession(APIView):
    serializer_class = SessionRequestSerializer
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(manual_parameters=[token_param_config,
                                            token_param_school,
                                            token_param_course_instance,
                                            token_param_session_type,
                                            token_param_programme
                                            ])



    def get(self, request):
        institute_fnid = request.query_params.get("institute_fnid", None)
        if not get_or_false(Institute, institute_fnid):
            return Response({'error': 'Institute not found'}, status=status.HTTP_400_BAD_REQUEST)

        # Get school_fnid if in query string
        school_fnid = request.query_params.get("school_fnid", None)
        if not get_or_false(School, school_fnid):
            return Response({'error': 'School not found'}, status=status.HTTP_400_BAD_REQUEST)

        # Get course_instance_fnid if in query string
        course_instance_fnid = request.query_params.get("course_instance_fnid", None)
        if not get_or_false(CourseInstance, course_instance_fnid):
            return Response({'error': 'Course Instance not found'}, status=status.HTTP_400_BAD_REQUEST)

        # Get programme_fnid if in query string
        programme_fnid = request.query_params.get("programme_fnid", None)
        if not get_or_false(Programme, programme_fnid):
            return Response({'error': 'Programme not found'}, status=status.HTTP_400_BAD_REQUEST)


        # Get all ongoing sessions
        filters_session = helpers.filters.build_filter_from_query_string(request, Session, expired_override=False)

        # Get all relevant students
        #filters_student = helpers.filters.build_filter_from_query_string(request, Student, active_override=True)

        if institute_fnid:
            
            # Get all ongoing sessions
            sessions_list = [x.fnid for x in Session.objects.filter(filters_session).filter(expired=False, cancelled=False)]

            # Filter if school specific
            if school_fnid:
                attendance_records_all = Attendance.objects.filter(school_fnid=school_fnid, session_fnid__in=sessions_list)
                sessions_list = list(set([x.session_fnid for x in attendance_records_all]))

            # Filter if programme specific
            elif programme_fnid:
                attendance_records_all = Attendance.objects.filter(programme_fnid=programme_fnid, session_fnid__in=sessions_list)
                sessions_list = list(set([x.session_fnid for x in attendance_records_all]))

            else:
                # Get all attendance records associated with ongoing sessions
                attendance_records_all = Attendance.objects.filter(
                session_fnid__in=sessions_list,
            )

            # Get all attendance records associated with ongoing sessions where students are present
            attendance_records_present = attendance_records_all.filter(present=True).count() + attendance_records_all.filter(present=False, approved_absence=True).count()

            sessions = Session.objects.filter(fnid__in=sessions_list)

            print("Attendance present:", attendance_records_present)

            # Calculate attendance percentage
            total_students = len(attendance_records_all)
            attending_students = attendance_records_present
            if total_students != 0:
                try:
                    attendance_percentage = float('{0:5g}'.format(attending_students * 100 / total_students))
                except ZeroDivisionError:
                    attendance_percentage = 0

            else:
                attendance_percentage = 0

            # Build JSON response data
            data = {
                "institute_fnid": institute_fnid,
                "school_fnid": school_fnid,
                "programme_fnid": programme_fnid,
                "course_instance_fnid": course_instance_fnid,
                "sessions_count": len(sessions),
                "total_students": total_students,
                "attending_students": attending_students,
                "attending_percentage": "{:.1f}".format(attendance_percentage)
            }

            return Response(data, status=status.HTTP_200_OK)

        else:
            return Response({'error': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)


class AttendanceOverview(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(manual_parameters=[token_param_config,
                                            token_param_school,
                                            token_param_course_instance,
                                            token_param_programme,
                                            token_param_min,
                                            token_param_max
                                            ])
    def get(self, request):
        institute_fnid = request.query_params.get("institute_fnid", None)

        # Get school_fnid if in query string
        school_fnid = request.query_params.get("school_fnid", None)

        # Get course_instance_fnid if in query string
        course_instance_fnid = request.query_params.get("course_instance_fnid", None)

        # Get programme_fnid if in query string
        programme_fnid = request.query_params.get("programme_fnid", None)

        # Get min value from query string
        min_value = request.query_params.get("min", 0)

        # Get max value if in query string
        max_value = request.query_params.get("max", 100)

        try:
            if course_instance_fnid:
                course_instance = CourseInstance.objects.get(fnid=course_instance_fnid)
                enrollments = CourseInstanceStudent.objects.filter(course_instance_fnid=course_instance_fnid)
                student_fnids = {enrollment.student_fnid: enrollment.average_attend_pc for enrollment in enrollments}
                total_students = len(student_fnids)

                if max_value == 100 or max_value == "100":
                    students_in_band = len([x for x in student_fnids.values() if x >= float(min_value) and x <= float(max_value)])
                else:
                    students_in_band = len([x for x in student_fnids.values() if x >= float(min_value) and x < float(max_value)])
                
                if total_students != 0:
                    band_percentage = (students_in_band / total_students) * 100
                else:
                    band_percentage = 0
                    
            else:
                

                # Get all active students
                filters_student = helpers.filters.build_filter_from_query_string(request, Student, active_override=True, full_range=True)

                if institute_fnid:

                    active_students_all = Student.objects.filter(filters_student)  

                    if max_value == 100 or max_value == "100":
                        active_students_band = active_students_all.filter(average_attend_pc__gte=min_value, average_attend_pc__lte=max_value)
                    else:
                        active_students_band = active_students_all.filter(average_attend_pc__gte=min_value, average_attend_pc__lt=max_value)

                    # Calculate band attendance percentage
                    total_students = len(active_students_all)
                    students_in_band = len(active_students_band)
                    if total_students != 0:
                        band_percentage = (students_in_band / total_students) * 100
                    else:
                        band_percentage = 0

            # Build JSON response data
            data = {
                "institute_fnid": institute_fnid,
                "school_fnid": school_fnid,
                "programme_fnid": programme_fnid,
                "course_instance_fnid": course_instance_fnid,
                "total_students": total_students,
                "students_in_band": students_in_band,
                "percentage": "{:.1f}".format(band_percentage),
                "min": min_value,
                "max": max_value
            }

            return Response(data, status=status.HTTP_200_OK)

        except:
            return Response({'error': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)
    
class CountActiveStudents(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(manual_parameters=[token_param_config,
                                            token_param_school,
                                            token_param_course_instance,
                                            token_param_programme
                                            ])
    def get(self, request):
        institute_fnid = request.query_params.get("institute_fnid", None)

        # Get school_fnid if in query string
        school_fnid = request.query_params.get("school_fnid", None)

        # Get course_instance_fnid if in query string
        course_instance_fnid = request.query_params.get("course_instance_fnid", None)

        # Get programme_fnid if in query string
        programme_fnid = request.query_params.get("programme_fnid", None)

        construct = [course_instance_fnid, programme_fnid, school_fnid]

        # Remove None values from construct
        construct = [x for x in construct if x != ""]

        if len(construct) > 1:
            return Response({'error': 'Only one optional parmeter permitted.'}, status=status.HTTP_400_BAD_REQUEST)

        # Get all active students
        filters_student = helpers.filters.build_filter_from_query_string(request, Student, active_override=True)
        print("Student Filters: ", filters_student)

        if institute_fnid:
            students = [x.fnid for x in Student.objects.filter(filters_student)]

            # Get all attendance records associated with ongoing sessions
            active_students_count = Student.objects.filter(filters_student).count()

            # Build JSON response data
            data = {
                "institute_fnid": institute_fnid,
                "school_fnid": school_fnid,
                "programme_fnid": programme_fnid,
                "course_instance_fnid": course_instance_fnid,
                "active_students": active_students_count
            }

            return Response(data, status=status.HTTP_200_OK)

        else:
            return Response({'error': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)



