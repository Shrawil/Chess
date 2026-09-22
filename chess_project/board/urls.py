from django.urls import path
from . import views

urlpatterns = [
    path("", views.board, name="home"),
    path("create/", views.create_room, name="create_room"),

    path(
        "room/<str:room_id>/",
        views.room,
        name="room"
    ),

    path(
        "room/<str:room_id>/state/",
        views.get_board,
        name="get_board"
    ),

    path(
        "room/<str:room_id>/move/",
        views.make_move,
        name="make_move"
    ),
]