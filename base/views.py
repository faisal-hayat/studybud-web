# imports 
from .forms import RoomForm
from django.db.models import Q
from .models import Room, Topic
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import HttpResponse, redirect, render, get_object_or_404

# ------------------------------------------------------------------------ #
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
# ------------------------------------------------------------------------ #
# Function for creating the room
@login_required(login_url='base:login')
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
# ------------------------------------------------------------------------ #
# Creaet view for updating the room 
@login_required(login_url='base:login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    
    # Only the creator of room can delete the room
    if request.user != room.host:
        return HttpResponse('You cant change the room content')

    # Create the form object 
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
# ------------------------------------------------------------------------ #
@login_required(login_url='base:login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=int(pk))

    # Only the creator of room can delete the room
    if request.user != room.host:
        return HttpResponse('You cant change the room content')

    if request.method == "POST":
        room.delete()
        return redirect('/base/')
    context = {
        'obj': room
    }
    return render(request, 'base/delete.html', context)
# ------------------------------------------------------------------------ #
def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('/base/')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        print(f'username is : {username}, and size is : {len(username)}, password is : {password}')
        # Use try catch block 
        try:
            user = User.objects.get(username=username)
            user = authenticate(request,
                    username=username,
                    password=password)
            if user is not None:
                login(request, user)
                # Redirect the user 
                return redirect('/base/')
            else:
                messages.error(request, 'user credential are not correct')
        except:
            # Throw the error message that user does not exit
            messages.error(request, 'user does not exist')
    context = {
        'page': page
    }
    return render(request, 'base/login_register.html', context)
# ------------------------------------------------------------------------ #
def logoutUser(request):
    logout(request) # This will delete the session token for the user
    return redirect('/base/')
# ------------------------------------------------------------------------ #
def registerPage(request):
    form = UserCreationForm()
    # Let's process the form
    if request.method == 'POST':
        f = UserCreationForm(request.POST)
        if f.is_valid():
            # save the form and freeze the user
            user = f.save(commit=False)
            user.username = user.username.lower()
            user.save()
            # login the user
            login(request, user=user)
            # redirect the user
            return redirect('/base/')
        else:
            messages.error(request, 'Something went wrong, please try again')
    context = {
        'form': form
    }
    return render(request, 'base/login_register.html', context)
# ------------------------------------------------------------------------ #