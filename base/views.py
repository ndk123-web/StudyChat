from django.shortcuts import render,redirect
from django.http import HttpRequest
from numpy import delete
from django.http import HttpResponse
from django.shortcuts import render
from .models import Room,Topic,Message
from .forms import RoomForm,UserForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

# It gives the Operations like and(&) , or(|) for database
from django.db.models import Q


def loginPage(req):
    
    page = 'login'
    
    if req.user.is_authenticated:
        return redirect('Home')
    
    if req.method == 'POST':
        username = req.POST.get('username')
        password = req.POST.get('password')
        
        user = authenticate(req, username=username, password=password)
        if user is not None:
            login(req, user)
            return redirect('Home')
        else:
            messages.error(req, 'Username or password is incorrect')
    
    context = {'page':page}
    return render(req,'login_register.html',context)

def logoutUser(req):
    logout(req)
    return redirect('Home')

def registerPage(req):
    if req.method == 'POST':
        username = req.POST.get('username')
        password = req.POST.get('password')
        confirm_password = req.POST.get('confirm_password')
        
        if password == confirm_password:
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, password=password)
                login(req, user)
                return redirect('Home')
            else:
                messages.error(req, 'User already exists')
        else:
            messages.error(req, 'Passwords do not match')
    
    context = {}
    return render(req, 'signup.html', context)

def home(req):
    q = req.GET.get('q')
    
    if q:
        # Checks atleast one character matched (icontains)
        # Room -> topic(Topic) -> name 
        rooms_base = Room.objects.filter(
            Q(topic__name__icontains=q) |
            Q(name__icontains=q) |
            Q(description__icontains=q) |
            Q(host__username__icontains=q)
        )         
    else:
        rooms_base = Room.objects.all()

    room_count = rooms_base.count()
    
    # Retrieves all the messages of the rooms_base 
    room_messages = Message.objects.filter(Q(room__in=rooms_base))
    
    topics = Topic.objects.all()
    context = {'rooms_base': rooms_base, 'topics': topics,'room_count':room_count,'room_messages':room_messages}
    return render(req, 'home.html', context)


def userProfile(req,pk):
    user = User.objects.get(id=pk)
    
    # It will get all rooms related to user id = pk
    rooms_base = user.room_set.all()
    room_messages = Message.objects.filter(user__username=user.username)
    topics = Topic.objects.all()
    context={'user':user,'rooms_base':rooms_base,'room_messages':room_messages,'topics':topics}
    return render(req,'profile.html',context)
    

def room(req,pk):   
    room = Room.objects.get(id=pk)
    
    # It will get all the messages of that room
    # It means give us all the set of messages that are related to that room 
    messages = room.message_set.all()  
    
    # It will get all the participants of that room
    # ManyToManyField is used to get all the participants of that room
    # Returns user objects of that room id 
    participants = room.participants.all()
    
    if req.method == 'POST':
        if req.POST.get('body') is not '':
            message = Message.objects.create(
                user = req.user,
                room = room ,
                body = req.POST.get('body')
            )
            room.participants.add(req.user)
             # it's necessary cause if we reload the page then it will not send the same data again
            return redirect('Room',pk=room.id)      
       
    context = {'room':room,'conversations':messages,'participants':participants}
    return render(req,'room.html',context)


@login_required(login_url = 'Login-Page')
def createRoom(req):
    form = RoomForm()
    topics = Topic.objects.all()
    
    if req.method == 'POST':
        topic_name = req.POST.get('topic')
        topic , created = Topic.objects.get_or_create(name=topic_name)
        
        Room.objects.create(
            host = req.user,
            topic = topic,
            name = req.POST.get('name'),
            description = req.POST.get('description'),
        )
        return redirect('Home')
    
    elif req.method == 'GET':
        context = {'form':form,'topics':topics}
        return render(req,'room_form.html',context)
    
@login_required(login_url = 'Login-Page')
def updateRoom(req, pk):
    
    # Get the Row where id = pk
    room = Room.objects.get(id=pk)
    topics = Topic.objects.all()
      
    # if req is POST 
    if req.method == 'POST':
        topic_name = req.POST.get('topic')
        topic , created = Topic.objects.get_or_create(name=topic_name)
        
        room.name = req.POST.get('name')
        room.topic = topic 
        room.description = req.POST.get('description')
        room.save()
        return redirect('Home')
    
        
        # create objects and pass
        # form = RoomForm(req.POST,instance=room) # instance = room there is no need to write
        
        # if form data is valid according to sql rules
        # if form.is_valid():
            
        #     # if yes then save the data into database
        #     form.save()
        #     return redirect('Home')
        
    # But if req is GET then we need to prefiiled data of that we click on edit
    # Using instance = room we can prefill the data of that we click on edit
    elif req.method == 'GET':
        form = RoomForm(instance=room)
    
    # It's necessary to see the Form structure 
    # Because it's necessary to see the fields of the form
    # Form Structure is defined and data sending to the room_form.html
    context = {'form':form,'topics':topics,'sp_room':room}
    
    # Return the room_form.html in current url (create-room)
    return render(req,'room_form.html',context)

   
@login_required(login_url = 'Login-Page')
def deleteRoom(req,pk):
    room = Room.objects.get(id=pk)
    
    if req.method == 'POST':
        room.delete()       # We can delete the row from database
        return redirect('Home')
    
    return render(req,'delete.html',{'obj':room})

    
@login_required(login_url = 'Login-Page')
def deleteMessage(req,pk):
    message = Message.objects.get(id=pk)
    
    if req.method == 'POST':
        message.delete()       # We can delete the row from database
        return redirect('Room',pk=message.room.id)
    
    return render(req,'delete.html',{'obj':message})

@login_required(login_url = 'Login-Page')
def updateUser(req):
    form = UserForm(instance=req.user) # For Get Request that values already prefilled    
    
    if req.method == 'POST':
        form = UserForm(req.POST,instance = req.user) # Filled automatically with current user data
        if form.is_valid():
            form.save()
            return redirect('user-Profile' , pk=req.user.id)
    
    context = {'form':form}
    return render(req,'update-user.html',context)

def topicMobile(req):
    
    q = req.GET.get('q')
    
    if q:
        topics = Topic.objects.filter(name__icontains=q)
    else:
        topics = Topic.objects.all()
        
    context={'topics':topics}
    return render(req,'topics.html',context)

def activityMobile(req):
    room_messages = Message.objects.all()
    context={'room_messages':room_messages}
    return render(req,'activity.html',context)