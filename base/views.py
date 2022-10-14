# imports 
from .forms import RoomForm
from .models import Room, Topic
from django.db.models import Q
from django.shortcuts import redirect, render, get_object_or_404


# Create your views here.
def home(request):
    # Get quesry set value from the request once user has clicked on any topic name
    # q = request.GET.get('q') if request.GET.get('q') != None else ''
    if request.GET.get('q') != None:
        q = request.GET.get('q')
    else:
        q = ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | 
        Q(name__icontains=q) |
        Q(description__icontains=q))
    # Calculate the room count 
    room_count = rooms.count()

    # Let's browser all the topics
    topics = Topic.objects.all()[:10]
    context = {
        'rooms': rooms,
        'topics': topics,
        'room_count': room_count
    }
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = get_object_or_404(Room, pk=int(pk))
    context = {
        'room': room
    }
    return render(request, 'base/room.html', context)

# Function for creating the room
def create_room(request):
    # Room forms will be used here
    form = RoomForm()
    if request.method == 'POST':
        f = RoomForm(request.POST)
        if f.is_valid():
            # Save the model
            f.save()
            # After saving the model, 
            return redirect('/base/')
            
    # Provide the context
    context = {
        'form': form
    }
    return render(request, 'base/room_form.html', context)


# Creaet view for updating the room 
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    # Create the form objec 
    form = RoomForm(instance=room) # This line will fill the form with data that we have in our database and it belong the object we are showing
    if request.method == "POST":
        f = RoomForm(request.POST, instance=room)
        if f.is_valid():
            # Save the form and redirect it to the main page
            f.save()
            return redirect('/base/')
    context = {
        'form': form
    }
    return render(request, 'base/room_form.html', context)

def deleteRoom(request, pk):
    room = Room.objects.get(id=int(pk))
    if request.method == "POST":
        room.delete()
        return redirect('/base/')
    context = {
        'obj': room
    }
    return render(request, 'base/delete.html', context)


