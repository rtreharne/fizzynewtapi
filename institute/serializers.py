from rest_framework.serializers import ModelSerializer
from institute.models import Institute, InstituteDomain, InstituteConfig, Term, Year, SessionType
from rest_framework import serializers

class InstituteSerializer(ModelSerializer):

    class Meta:
        model = Institute
        fields = ('fnid', 'name',)

        read_only_fields = ['fnid']

class InstituteDomainSerializer(ModelSerializer):


    def validate(self, data):
        institute_fnid = data["institute_fnid"]
        # Raise error if institute doesn't exist
        try:
            Institute.objects.get(fnid=institute_fnid)
        except:
            raise serializers.ValidationError("This institute does not exist")

        return data


    class Meta:
        model = InstituteDomain
        fields = ('fnid', 'institute_fnid', 'domain', 'primary')

        read_only_fields = ['fnid']


class InstituteConfigSerializer(ModelSerializer):

    class Meta:
        model = InstituteConfig
        fields = ('fnid', 'institute_fnid', 'student_id_required', "term_start_week")

        read_only_fields = ['fnid']

class TermSerializer(ModelSerializer):

    class Meta:
        model = Term
        fields = ('fnid', 'institute_fnid', 'label', 'start_date', 'end_date', 'registration_start')

        read_only_fields = ['fnid']

class YearSerializer(ModelSerializer):

    class Meta:
        model = Year
        fields = ('fnid', 'institute_fnid', 'label',)

        read_only_fields = ['fnid']

class SessionTypeSerializer(ModelSerializer):

    class Meta:
        model = SessionType
        fields = ('fnid', 'institute_fnid', 'label')

        read_only_fields = ['fnid']