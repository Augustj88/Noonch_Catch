from http.client import HTTPResponse
from django.shortcuts import render
from .models import Room
from django.http import JsonResponse
import json
# from chat.models import UserGroup
def index(request):
    # users = UserGroup.objects.all()
    # room = request.POST.get('roomname', '')
    return render(request, 'chat/index.html')
    # return render(request, 'chat/index.html', {'users': users})

def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })
def ending(request):
    return render(request, 'chat/ending.html')

def get_user(request):
    roomname = json.loads(request.body.decode('utf-8'))
    roomname = roomname['roomname']
    rooms = Room.objects.filter(roomname=roomname)
    users = {}
    for i, room in enumerate(rooms):
        users[i] = room.nickname
    return JsonResponse(users)