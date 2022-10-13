from . import views
from django.urls import path


app_name = 'base'
urlpatterns = [
    # ex: localhots:8000/base/
    path("", view=views.home, name='home'),
    # ex: /base/room/1
    path('room/<str:pk>/', view=views.room, name='room'),
    # ex: /base/create_room
    path('create_room/', view=views.create_room, name='create-room'),
]