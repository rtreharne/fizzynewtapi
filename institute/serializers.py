from rest_framework.serializers import ModelSerializer
from institute.models import Institute

class InstituteSerializer(ModelSerializer):
    class Meta:
        model = Institute
        fields = ('name',)

        #read_only_fields = ['fnid']
