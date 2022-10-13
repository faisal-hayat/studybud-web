# imports 
from .models import Room
from .forms import RoomForm
from django.shortcuts import redirect, render, get_object_or_404


# Create your views here.
def home(request):
    rooms = Room.objects.all()[:5]
    context = {
        'rooms': rooms
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