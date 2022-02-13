from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

tasks = []
completed_tasks = []

def task_view(request):
    return render(request, "tasks.html", {"tasks": tasks})

def add_task_view(request):
    task_value = request.GET.get("task")
    tasks.append(task_value)
    return HttpResponseRedirect("/tasks")

def delete_task_view(request, index):
    del tasks[index-1]
    return HttpResponseRedirect("/tasks")

def done_task_view(request, index):
    done_task = tasks.pop(index-1)
    completed_tasks.append(done_task)
    return HttpResponseRedirect("/tasks")

def completed_task_view(request):
    return render(request, "completed.html", {"completed_task": completed_tasks})

def all_task_view(request):
    return render(request, "all.html", {"tasks": tasks, "completed_tasks": completed_tasks})

