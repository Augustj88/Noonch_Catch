from http.client import HTTPResponse
from django.shortcuts import render
from .models import Room,Pic
from django.http import JsonResponse
import json
import random
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

def post_pic(request):

    if request.method == 'POST':
        text = request.POST["text"]
        print(text)
        pk = random.randrange(0, 4)
        # question_num = Pic.objects.get(pk=pk)
        # question_url = question_num.url
        # question_answer = question_num.answer
        # test1 = Pic.objects.order_by('?').first().url
        test2 = Pic.objects.all()
        test_len = len(test2)
        test_random = random.randrange(0,test_len)
        test3 = test2[test_random]
        test_answer = test3.answer
        test_url = test3.url
        print(test_answer)
        print(test_url)

    return JsonResponse({'test_url':test_url,'test_answer':test_answer})

#
# def get_pic(request):
#     if request.method == 'GET':
#         pk = random.randrange(0,4)
#         question_num = Pic.objects.get(pk=pk)
#         question_url = question_num.url
#         question_answer = question_num.answer
#
#     return render(request, 'chat/room.html',{'question_url':question_url, 'question_answer':question_answer})
#
