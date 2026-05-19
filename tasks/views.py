from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .models import Task
from .forms import TaskForm, RegisterForm


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            login(request, user)
            return redirect('/')
    else:
        form = RegisterForm()

    return render(request, 'tasks/register.html', {'form': form})


@login_required
def dashboard(request):
    tasks = Task.objects.filter(user=request.user)

    context = {
        'total': tasks.count(),
        'active': tasks.filter(completed=False).count(),
        'done': tasks.filter(completed=True).count()
    }

    return render(request, 'tasks/dashboard.html', context)


@login_required
def task_list(request):
    status = request.GET.get('status')

    tasks = Task.objects.filter(user=request.user)

    if status == 'done':
        tasks = tasks.filter(completed=True)
    elif status == 'active':
        tasks = tasks.filter(completed=False)

    return render(request, 'tasks/task_list.html', {'tasks': tasks})


@login_required
def task_create(request):
    form = TaskForm(request.POST or None)

    if form.is_valid():
        task = form.save(commit=False)
        task.user = request.user
        task.save()
        return redirect('/tasks/')

    return render(request, 'tasks/task_form.html', {'form': form})


@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)

    form = TaskForm(request.POST or None, instance=task)

    if form.is_valid():
        form.save()
        return redirect('/tasks/')

    return render(request, 'tasks/task_form.html', {'form': form})


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return redirect('/tasks/')