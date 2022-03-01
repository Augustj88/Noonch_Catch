from django.db import models


#
class Room(models.Model):
    roomname = models.CharField(max_length=20)
    nickname = models.CharField(max_length=20)
