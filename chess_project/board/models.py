from django.db import models


class Room(models.Model):
    room_id = models.CharField(max_length=8, unique=True)
    white = models.CharField(max_length=40, null=True, blank=True)
    black = models.CharField(max_length=40, null=True, blank=True)
    fen = models.TextField(default="")

    def __str__(self):
        return self.room_id