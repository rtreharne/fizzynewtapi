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

class ConsecutiveAbsence(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(manual_parameters=[
        token_param_config,
        token_param_start,
        token_param_n,
        token_param_school,
        token_param_programme,
        token_param_course_instance,
    ])
    def get(self, request):
        institute_fnid = request.query_params.get("institute_fnid", None)
        date = request.query_params.get("after", None)
        n = request.query_params.get("n", None)

        if date is None or "":
            print("Date: ", date)
            return Response({'error': 'After datetime (consecutive absences) must be supplied in query string.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if n is None or "" or not n.isdigit():
            return Response({'error': 'n (consecutive absences) must be supplied as integer in query string.'}, status=status.HTTP_400_BAD_REQUEST)

        
        school_fnid = request.query_params.get("school_fnid", None) 
        programme_fnid = request.query_params.get("programme_fnid", None)
        course_instance_fnid = request.query_params.get("course_instance_fnid", None)

        # Get all expired sessions
        if date:
            sessions_filter = helpers.filters.build_filter_from_query_string(request, Session, expired_override=True)
            sessions = Session.objects.filter(sessions_filter)
        else:
            # Get date 30 days ago in iso format
            date = datetime.now() - timedelta(days=30)
            print("DATE: ", date)
            date = date.isoformat()
            sessions_filter = helpers.filters.build_filter_from_query_string(request, Session, expired_override=True)
            sessions = Session.objects.filter(sessions_filter).filter(session_start__gte=date)

        if course_instance_fnid:
            enrollments = CourseInstanceStudent.objects.filter(course_instance_fnid=course_instance_fnid)
            student_fnids = [enrollment.student_fnid for enrollment in enrollments]
            students = Student.objects.filter(fnid__in=student_fnids)
        else:
            student_filters = helpers.filters.build_filter_from_query_string(request, Student)
            student_fnids = [x.fnid for x in Student.objects.filter(student_filters)]
            students = Student.objects.filter(fnid__in=student_fnids)

        cause_for_concern = []
        for student in students:
            attendance_records = Attendance.objects.filter(student_fnid=student.fnid, session_fnid__in=sessions).order_by('-created_at')
            if len(attendance_records) > 0:
                # Loop over attendance records and count number of consecutive present=False
                consecutive_missed = 0
                for attendance_record in attendance_records:
                    if attendance_record.present == False:
                        consecutive_missed += 1
                    else:
                        break
                if consecutive_missed >= int(n):
                    cause_for_concern_student = {
                        "student_fnid": student.fnid,
                        "student_id": student.student_id,
                        "last_name": student.last_name,
                        "first_name": student.first_name,
                        "consecutive_absence": consecutive_missed,
                        "average_attend_pc": student.average_attend_pc
                    }
                    cause_for_concern.append(cause_for_concern_student)

        data = cause_for_concern

        return Response(data, status=status.HTTP_200_OK)
    
class AttendanceThreshold(APIView):
    """
    Returns students who have attendance below a certain threshold
    """
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(manual_parameters=[
        token_param_config,
        token_param_threshold,
        token_param_school,
        token_param_programme,
        token_param_course_instance,
    ])
    def get(self, request):

        try:
            institute_fnid = request.query_params.get("institute_fnid", None)

            if institute_fnid:
                threshold = request.query_params.get("threshold", None)
                
                if threshold is None or "" or not threshold.isdigit():
                    return Response({'error': 'Threshold value must be supplied as int in query string.'}, status=status.HTTP_400_BAD_REQUEST)

                course_instance_fnid = request.query_params.get("course_instance_fnid", None)

                if course_instance_fnid:
                    enrollments = CourseInstanceStudent.objects.filter(course_instance_fnid=course_instance_fnid)
                    student_fnids = [enrollment.student_fnid for enrollment in enrollments]
                    students = Student.objects.filter(fnid__in=student_fnids).filter(active=True).order_by('last_name')
                else:
                    student_filters = helpers.filters.build_filter_from_query_string(request, Student)
                    student_fnids = [x.fnid for x in Student.objects.filter(student_filters)]
                    students = Student.objects.filter(fnid__in=student_fnids).filter(active=True).order_by('last_name')

                cause_for_concern = []
                for student in students:
                    if student.average_attend_pc < float(threshold):
                        cause_for_concern_student = {
                            "student_fnid": student.fnid,
                            "student_id": student.student_id,
                            "last_name": student.last_name,
                            "first_name": student.first_name,
                            "average_attend_pc": student.average_attend_pc
                        }
                        cause_for_concern.append(cause_for_concern_student)
                    
                data = cause_for_concern

                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'institute_fnid not supplied'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'error': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)
    



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


class SchoolCount(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        institute_fnid = request.query_params.get("institute_fnid", None)

        if institute_fnid:
            schools = School.objects.filter(institute_fnid=institute_fnid, active=True)
            school_count = schools.count()

            # Build JSON response data
            data = {
                "institute_fnid": institute_fnid,
                "school_count": school_count
            }

            return Response(data, status=status.HTTP_200_OK)

        else:
            return Response({'error': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)
        
class ProgrammeCount(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(manual_parameters=[token_param_config,
                                            token_param_school])
    def get(self, request):
        institute_fnid = request.query_params.get("institute_fnid", None)

        if institute_fnid:
            programme_filters = helpers.filters.build_filter_from_query_string(request, Programme)
            programmes = Programme.objects.filter(programme_filters).filter(active=True)
            programme_count = programmes.count()

            # Build JSON response data
            data = {
                "institute_fnid": institute_fnid,
                "programme_count": programme_count
            }

            return Response(data, status=status.HTTP_200_OK)

        else:
            return Response({'error': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)

class CourseInstanceCount(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(manual_parameters=[token_param_config,
                                            token_param_school])
    def get(self, request):
        institute_fnid = request.query_params.get("institute_fnid", None)
        school_fnid = request.query_params.get("school_fnid", None)

        if institute_fnid:

            if school_fnid:
                # Get all students in school
                student_filters = helpers.filters.build_filter_from_query_string(request, Student)
                student_fnids = [x.fnid for x in Student.objects.filter(student_filters)]
                enrollments = CourseInstanceStudent.objects.filter(student_fnid__in=student_fnids)
                course_instance_fnids = [enrollment.course_instance_fnid for enrollment in enrollments]
                course_instances = CourseInstance.objects.filter(fnid__in=course_instance_fnids, active=True)
                course_instance_count = course_instances.count()
            else:
                course_instances = CourseInstance.objects.filter(institute_fnid=institute_fnid, active=True)
                course_instance_count = course_instances.count()

            # Build JSON response data
            data = {
                "institute_fnid": institute_fnid,
                "course_instance_count": course_instance_count
            }

            return Response(data, status=status.HTTP_200_OK)
        
        else:
            return Response({'error': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)




