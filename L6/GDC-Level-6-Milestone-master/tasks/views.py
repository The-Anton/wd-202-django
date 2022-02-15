from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from tasks.models import Task

completed_tasks = []
tasks = []

def task_view(request):
    tasks = Task.objects.filter(deleted=False)
    search_term = request.GET.get("search")

    if search_term:
        tasks = tasks.filter(title__icontains=search_term)
    return render(request, "tasks.html", {"tasks": tasks})

def add_task_view(request):
    task_value = request.GET.get("task")
    Task(title=task_value).save()
    tasks.append(task_value)
    return HttpResponseRedirect("/tasks")

def delete_task_view(request, index):
    Task.objects.filter(id=index).update(deleted=True)
    return HttpResponseRedirect("/tasks")

def done_task_view(request, index):
    Task.objects.filter(id=index).update(completed=True)
    return HttpResponseRedirect("/tasks")

def completed_task_view(request):
    completed_tasks = Task.objects.all().filter(completed=True)
    return render(request, "completed.html", {"completed_tasks": completed_tasks})

def all_task_view(request):
    tasks = Task.objects.filter(deleted=False)
    completed_tasks = Task.objects.all().filter(completed=True)
    return render(request, "all.html", {"tasks": tasks, "completed_tasks": completed_tasks})

