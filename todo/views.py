from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import ToDoForm
from .models import ToDo, Project
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def signupuser(request):
    if request.method == "GET":
        return render(request, 'todo/signupuser.html', {'form': UserCreationForm})
    elif request.method == "POST":
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currenttodos')
            except IntegrityError:
                return render(request, 'todo/signupuser.html',
                              {'form': UserCreationForm, 'error': 'Username allready in use.'})
        else:
            return render(request, 'todo/signupuser.html',
                          {'form': UserCreationForm, 'error': 'Password did not match.'})

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', {'form': AuthenticationForm})

    elif request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/loginuser.html', {'form': AuthenticationForm, 'error': 'Invalide'})
        else:
            login(request, user)
            return redirect('home')


def home(request):
    projects = Project.objects.all()
    return render(request, 'todo/home.html', {'projects':projects})


##ToDos
@login_required
def currenttodos(request):
    todos = ToDo.objects.filter(user=request.user, completed__isnull=True)
    return render(request, 'todo/currenttodos.html', {'todos': todos})

@login_required
def createtodos(request):
    if request.method == 'GET':
        return render(request, 'todo/createtodos.html', {'form': ToDoForm})
    elif request.method == 'POST':
        try:
            form = ToDoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/createtodos.html', {'form': ToDoForm, 'error': 'Bad Data passed. Try again'})

@login_required
def viewtodo(request, todo_pk):
    todo = get_object_or_404(ToDo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = ToDoForm(instance=todo)
        return render(request, 'todo/viewtodo.html', {'todo': todo, 'form': form})
    elif request.method == 'POST':
        try:
            form = ToDoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/viewtodos.html',
                          {'todo': todo, 'form': ToDoForm, 'error': 'Bad Data passed. Try again'})

@login_required
def completetodo(request, todo_pk):
    todo = get_object_or_404(ToDo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.completed = timezone.now()
        todo.save()
        return redirect('currenttodos')
@login_required
def deletetodo(request, todo_pk):
    todo = get_object_or_404(ToDo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')
@login_required
def completedtodos(request):
    todos = ToDo.objects.filter(user=request.user, completed__isnull=False).order_by('-completed')
    return render(request, 'todo/completedtodos.html', {'todos': todos})