
from django.shortcuts import render,redirect
from .models import Room
# Create your views here.
def room(request):
    if request.method=="POST":
        username = request.POST.get('username')
        room_name = request.POST.get('room_id')
        print(username, room_name)
        try:
            getroom = Room.objects.get(name=room_name)
            print("Room exists:", getroom.name)
        except  Room.DoesNotExist:
            new_room = Room(name=room_name)
            new_room.save()
            print("New room created:", new_room.name)
        return redirect('room', username=username, room_name=room_name)
    return render(request, 'room.html')

def message(request,username,room_name):
    messages = Room.objects.get(name=room_name).messages.all()
    context = {
        'username': username,
        'room_name': room_name,
        'messages': messages,
    }
    return render(request, 'message.html', context)