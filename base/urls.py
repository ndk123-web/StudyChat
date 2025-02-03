from django.urls import path,include
from . import views 

urlpatterns = [
    path('',views.home,name="Home"),
    path('room/<int:pk>',views.room,name='Room'),
    path('create-room/',views.createRoom,name='create-Room'),
    path('update-room/<int:pk>/',views.updateRoom,name='update-Room'),
    path('delete-room/<int:pk>/',views.deleteRoom,name='delete-Room'),
    path('login/',views.loginPage,name='Login-Page'),
    path('logout/',views.logoutUser,name='Logout-Page'),
    path('register/',views.registerPage,name='Register-Page'),
    path('delete-message/<int:pk>',views.deleteMessage,name='delete-Message'),
    path('user-profile/<int:pk>',views.userProfile,name='user-Profile'),
    path('update-user',views.updateUser,name='update-User'),
    path('topic/',views.topicMobile,name='topics-Mobile'),
    path('activity',views.activityMobile,name = 'activity-Mobile'),
]