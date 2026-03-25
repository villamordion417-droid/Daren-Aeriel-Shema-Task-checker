from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Task
from .forms import CustomUserCreationForm, CustomAuthenticationForm

def landing_view(request):
    return render(request, 'tasks/landing.html')

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('task_dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'tasks/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('task_dashboard')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'tasks/login.html', {'form': form})

@login_required
def task_dashboard(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            Task.objects.create(user=request.user, title=title)
        return redirect('task_dashboard')
    tasks = Task.objects.filter(user=request.user, is_completed=False)
    return render(request, 'tasks/tasks.html', {'tasks': tasks})

@login_required
@require_POST
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.is_completed = True
    task.save()
    return JsonResponse({'status': 'ok'})

@login_required
@require_POST
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    return JsonResponse({'status': 'ok'})
