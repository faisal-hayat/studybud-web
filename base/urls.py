from . import views
from django.urls import path


app_name = 'base'
urlpatterns = [
    # ex: localhots:8000/base/
    path("", view=views.home, name='home'),
    # ex: /base/room/1
    path('room/<str:pk>/', view=views.room, name='room'),
    # ex: /base/create_room
    path('create-room/', view=views.create_room, name='create-room'),
    # ex: /base/update-roon/1
    path('update-room/<str:pk>', view=views.updateRoom, name='update-room'),
    # ex: /base/delete-roon/1
    path('delete-room/<str:pk>', view=views.deleteRoom, name='delete-room'),
    # ex: base/login
    path('login/', view=views.loginPage, name='login'),
    # ex: base/logout
    path('logout/', view=views.logoutUser, name='logout')
]