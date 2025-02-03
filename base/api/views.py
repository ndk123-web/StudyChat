from rest_framework.decorators import api_view
from rest_framework.response import Response      # Any iterator that returns dictionary (JSON)
from rest_framework.serializers import Serializer # Any Model that converts into JSON  
from base.models import Room
from .serializers import RoomModel                # Logic is written here

@api_view(['GET'])
def getRoutes(req):
    routes = [
        'GET /api/',
        'GET /api/rooms',
        'GET /api/rooms/:id'
    ]    
    return Response(routes)
    
@api_view(['GET'])
def getRooms(req):
    # RoomModel is a serializer that converts Room model instances into JSON (or dict format)
    rooms = Room.objects.all()  # Fetch all Room instances (queryset)
    
    # many=False means we are serializing a single object (default behavior).
    # many=True means we are serializing multiple objects (like a queryset).
    serializer = RoomModel(rooms, many=True)  # Serialize the queryset of rooms into JSON (list of dictionaries)
    
    # serializer.data returns a list of dictionaries, each representing a Room object.
    return Response(serializer.data)  # Return the serialized data as the response

@api_view(['GET'])
def getRoom(req,pk):
    room = Room.objects.get(id=pk)
    serializer = RoomModel(room,many=False)
    return Response(serializer.data)