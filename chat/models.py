from django.db import models


class Room(models.Model):
    roomname = models.CharField(max_length=20)
    nickname = models.CharField(max_length=20)

class Pic(models.Model):
    answer = models.CharField(max_length=20)
    url = models.URLField(max_length=2000)