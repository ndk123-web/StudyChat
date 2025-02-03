from django.urls import URLPattern, path 
from . import views

urlpatterns = [
    path('',views.getRoutes,name='get-route'),
    path('rooms/',views.getRooms,name='get-rooms'),
    path('rooms/<int:pk>',views.getRoom,name='get-Room')
]
