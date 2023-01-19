from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from attendance.serializers import SessionRequestSerializer, SessionSerializer, AttendanceSerializer
from course.serializers import CourseInstanceSerializer
from course.models import CourseInstance
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from attendance.models import SessionRequest, Session, Attendance
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import exceptions
from course.models import CourseInstanceStudent
from student.models import Student
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from institute.models import Institute
from datetime import datetime
from rest_framework.views import APIView
from rest_framework import status

token_param_start = openapi.Parameter('after', in_=openapi.IN_QUERY, description="filter for session requests that started after this datetime", type=openapi.FORMAT_DATETIME)
token_param_end = openapi.Parameter('before', in_=openapi.IN_QUERY, description="filter for session requests that started before this datetime", type=openapi.FORMAT_DATETIME)
token_param_config=openapi.Parameter('institute_fnid', in_=openapi.IN_QUERY, description="This parameter must be included in the query string of every call.", type=openapi.TYPE_STRING)



def json_datetime_to_python(json_dt):
    try:
        return datetime.strptime(json_dt, "%Y-%m-%dT%H:%M:%SZ")
    except:
        return json_dt

class AttendanceBySession(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, institute_fnid=None, session_fnid=None):

        try:
            institute = Institute.objects.get(fnid=institute_fnid)
        except:
            return Response({'error': 'Institute does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            session = Session.objects.get(fnid=session_fnid)
        except:
            return Response({'error': 'Session does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        queryset = Attendance.objects.filter(institute_fnid=institute_fnid, session_fnid=session_fnid)

        serializer = AttendanceSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AttendanceBySessionByStudent(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, institute_fnid=None, session_fnid=None, student_fnid=None):

        try:
            institute = Institute.objects.get(fnid=institute_fnid)
        except:
            return Response({'error': 'Institute does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            session = Session.objects.get(fnid=session_fnid)
        except:
            return Response({'error': 'Session does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            session = Student.objects.get(fnid=student_fnid)
        except:
            return Response({'error': 'Student does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        queryset = Attendance.objects.filter(institute_fnid=institute_fnid, session_fnid=session_fnid, student_fnid=student_fnid)

        serializer = AttendanceSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ActiveSessionRequestStudent(APIView):
    serializer_class = SessionRequestSerializer
    permission_classes = (IsAuthenticated,)

    def filter_by_datetime(self, request, queryset):
        if request.GET.get("after", False):
            try:
                queryset = queryset.filter(session_start__gte=json_datetime_to_python(request.GET["after"]))
            except:
                pass

        if request.GET.get("before", False):
            try:
                queryset = queryset.filter(session_start__lte=json_datetime_to_python(request.GET["before"]))
            except:
                pass

        return queryset

    @swagger_auto_schema(manual_parameters=[token_param_start, token_param_end])
    def get(self, request, institute_fnid=None, student_fnid=None):


        try:
            institute = Institute.objects.get(fnid=institute_fnid)
        except:
            return Response({'error': 'Institute does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            student = Student.objects.get(fnid=student_fnid)
        except:
            return Response({'error': 'Student does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        queryset = SessionRequest.objects.filter(institute_fnid=institute_fnid, student_fnid=student_fnid, expired=False)
        queryset = self.filter_by_datetime(request, queryset)

        serializer = SessionRequestSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ActiveSessionStudent(APIView):
    permission_classes = (IsAuthenticated,)

    def filter_by_datetime(self, request, queryset):
        if request.GET.get("after", False):
            try:
                queryset = queryset.filter(session_start__gte=json_datetime_to_python(request.GET["after"]))
            except:
                pass

        if request.GET.get("before", False):
            try:
                queryset = queryset.filter(session_start__lte=json_datetime_to_python(request.GET["before"]))
            except:
                pass

        return queryset

    @swagger_auto_schema(manual_parameters=[token_param_start, token_param_end])
    def get(self, request, institute_fnid=None, student_fnid=None):


        try:
            institute = Institute.objects.get(fnid=institute_fnid)
        except:
            return Response({'error': 'Institute does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            student = Student.objects.get(fnid=student_fnid)
        except:
            return Response({'error': 'Student does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        session_ids = [x.session_fnid for x in Attendance.objects.filter(institute_fnid=institute_fnid, student_fnid=student_fnid)]

        queryset = Session.objects.filter(fnid__in=session_ids)
        queryset = self.filter_by_datetime(request, queryset)

        serializer = SessionSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ActiveSessionRequestCourseInstance(APIView):
    serializer_class = CourseInstanceSerializer
    permission_classes = (IsAuthenticated,)

    def filter_by_datetime(self, request, queryset):
        if request.GET.get("after", False):
            try:
                queryset = queryset.filter(session_start__gte=json_datetime_to_python(request.GET["after"]))
            except:
                pass

        if request.GET.get("before", False):
            try:
                queryset = queryset.filter(session_start__lte=json_datetime_to_python(request.GET["before"]))
            except:
                pass

        return queryset

    @swagger_auto_schema(manual_parameters=[token_param_start, token_param_end])
    def get(self, request, institute_fnid=None, course_instance_fnid=None):

        try:
            institute = Institute.objects.get(fnid=institute_fnid)
        except:
            return Response({'error': 'Institute does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            course_instance = CourseInstance.objects.get(fnid=course_instance_fnid)
        except:
            return Response({'error': 'Student does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        queryset = SessionRequest.objects.filter(institute_fnid=institute_fnid, course_instance_fnid=course_instance_fnid, expired=False)
        queryset = self.filter_by_datetime(request, queryset)

        serializer = SessionRequestSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ActiveSessionCourseInstance(APIView):
    permission_classes = (IsAuthenticated,)

    def filter_by_datetime(self, request, queryset):
        if request.GET.get("after", False):
            try:
                queryset = queryset.filter(session_start__gte=json_datetime_to_python(request.GET["after"]))
            except:
                pass

        if request.GET.get("before", False):
            try:
                queryset = queryset.filter(session_start__lte=json_datetime_to_python(request.GET["before"]))
            except:
                pass

        return queryset

    @swagger_auto_schema(manual_parameters=[token_param_start, token_param_end])
    def get(self, request, institute_fnid=None, course_instance_fnid=None):

        try:
            institute = Institute.objects.get(fnid=institute_fnid)
        except:
            return Response({'error': 'Institute does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            course_instance = CourseInstance.objects.get(fnid=course_instance_fnid)
        except:
            return Response({'error': 'Student does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        queryset = Session.objects.filter(institute_fnid=institute_fnid, course_instance_fnid=course_instance_fnid, expired=False)
        queryset = self.filter_by_datetime(request, queryset)

        serializer = SessionSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ListCreateSessionRequestAPIView(ListCreateAPIView):
    serializer_class = SessionRequestSerializer
    permission_classes = (IsAuthenticated,)

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["fnid",
                        "institute_fnid",
                        "student_fnid",
                        "course_instance_fnid",
                        "expired"
                        ]

    def perform_create(self, serializer):
        new_object = serializer.save()
        return new_object

    def get_queryset(self):
        queryset = SessionRequest.objects.all()
        # Check this!
        # print(len(queryset)) This is important!
        institute_fnid = self.request.query_params.get("institute_fnid", None)
        if institute_fnid:
            return queryset
        else:
            raise exceptions.ParseError("institute_fnid not supplied in query string.")

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class SessionRequestDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = SessionRequestSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    lookup_field = "fnid"

    filterset_fields = ["institute_fnid"]

    def get_queryset(self):

        queryset = SessionRequest.objects.all()
        institute_fnid = self.request.query_params.get("institute_fnid", None)
        if institute_fnid:
            queryset = queryset.filter(institute_fnid=institute_fnid)
        else:
            raise exceptions.ParseError("institute_id not supplied in query string.")
        return queryset


class ListCreateSessionAPIView(ListCreateAPIView):
    serializer_class = SessionSerializer
    permission_classes = (IsAuthenticated,)

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["fnid",
                        "institute_fnid",
                        "course_instance_fnid",
                        "session_start",
                        "session_audit",
                        ]

    def perform_create(self, serializer):
        new_object = serializer.save()

        # create records for all
        class_list = CourseInstanceStudent.objects.filter(course_instance_fnid=new_object.course_instance_fnid)
        for student in class_list:
            print("student: ", student.__dict__)
            student_info = Student.objects.get(fnid=student.student_fnid)
            print("Updating attendance table")
            attendance = Attendance(
                institute_fnid=student.institute_fnid,
                school_fnid=student_info.school_fnid,
                course_instance_fnid=student.course_instance_fnid,
                session_fnid=new_object.fnid,
                student_fnid=student.student_fnid,
                session_type_fnid=new_object.session_type_fnid
            )
            print("nearly there")
            try:
                attendance.save()
            except:
                print("error saving attendance record")
        return new_object

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)



    def get_queryset(self):
        queryset = Session.objects.all()
        institute_fnid = self.request.query_params.get("institute_fnid", None)
        if institute_fnid:
            return queryset
        else:
            raise exceptions.ParseError("institute_fnid not supplied in query string.")


class SessionDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = SessionSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    lookup_field = "fnid"

    filterset_fields = ["institute_fnid"]

    def get_queryset(self):

        queryset = Session.objects.all()
        institute_fnid = self.request.query_params.get("institute_fnid", None)
        if institute_fnid:
            return queryset
            #queryset = queryset.filter(institute_fnid=institute_fnid)
        else:
            raise exceptions.ParseError("institute_id not supplied in query string.")
        return queryset


class ListCreateAttendanceAPIView(ListCreateAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = (IsAuthenticated,)

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["fnid",
                        "institute_fnid",
                        "student_fnid",
                        "course_instance_fnid",
                        "session_fnid",
                        "session_type_fnid"
                        ]

    def perform_create(self, serializer):
        new_object = serializer.save()
        return new_object

    def get_queryset(self):
        queryset = Attendance.objects.all()
        institute_fnid = self.request.query_params.get("institute_fnid", None)
        if institute_fnid:
            return queryset
        else:
            raise exceptions.ParseError("institute_fnid not supplied in query string.")


class AttendanceDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    lookup_field = "fnid"

    filterset_fields = ["institute_fnid", "school_fnid", "course_instance_fnid",
                        "session_fnid", "student_fnid", "session_type_fnid"]

    def get_queryset(self):

        queryset = Attendance.objects.all()
        institute_fnid = self.request.query_params.get("institute_fnid", None)
        if institute_fnid:
            queryset = queryset.filter(institute_fnid=institute_fnid)
        else:
            raise exceptions.ParseError("institute_id not supplied in query string.")
        return queryset



