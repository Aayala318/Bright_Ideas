from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from .models import Ideas
import bcrypt

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == "GET":
        return redirect('/')
    errors = User.objects.validate(request.POST)
    if errors:
        for e in errors.values():
            messages.error(request, e)
        return redirect('/')
    else:
        hash_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        alias = request.POST['alias'],
        email = request.POST['email'],
        password = hash_pw
        )
        request.session['user_id'] = new_user.id
        messages.success(request, "You have successfully registered!")
        return redirect('/display_all')

def login(request):
    if request.method == "GET":
        return redirect('/')
    if not User.objects.authenticate(request.POST['email'], request.POST['password']):
        messages.error(request, 'Invalid Email/Password')
        return redirect('/')
    user = User.objects.get(email=request.POST['email'])
    request.session['user_id'] = user.id
    messages.success(request, "You have successfully logged in!")
    return redirect('/display_all')

def logout(request):
    request.session.clear()
    return redirect('/')

def display_all(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'ideas': Ideas.objects.all(),
        'user': User.objects.get(id=request.session['user_id'])
    }    
    return render(request, 'display_all.html', context)
    

def create(request):
    errors = Ideas.objects.ideas(request.POST)
    if errors:
        for (key, value) in errors.items():
            messages.error(request, value)
        return redirect('/display_all')
    else:
        thisIdeas=Ideas.objects.create(
            description = request.POST['description'],
            owner_id = request.session['user_id']
        )
        user = User.objects.get(id=request.session['user_id'])
        thisIdeas.like.add(user)
    return redirect('/display_all')

def delete(request, id):
    idea = Ideas.objects.get(id=id)
    idea.delete()
    return redirect('/display_all')

def first_name(request, id):
    ideas = Ideas.objects.get(id=id)
    user = User.objects.get(id=request.session['user_id'])
    company.members.add(user)
    return redirect('/display_all')

def display_one(request, id):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'one_idea' : Ideas.objects.get(id=id),
    }    
    return render(request, 'display_one.html', context)

def liked_ideas(request, id):
    idea = Ideas.objects.get(id=id)
    user = User.objects.get(id=request.session['user_id'])
    idea.like.add(user)
    return redirect('/display_all')

def one_user(request, id):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=id)
    ideas = Ideas.objects.filter(owner=user)
    context = {
        'user' : User.objects.get(id=id),
        'ideas' : ideas
    }
    return render(request, 'user.html', context)