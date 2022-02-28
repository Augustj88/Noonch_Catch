from django.shortcuts import render
#
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