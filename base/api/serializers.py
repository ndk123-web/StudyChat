from rest_framework.serializers import ModelSerializer  # Converts Model instances into JSON Format
from base.models import Room

class RoomModel(ModelSerializer):
    class Meta:
        model = Room 
        fields ='__all__'