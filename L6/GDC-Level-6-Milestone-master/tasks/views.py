from re import template
from django.forms import ModelForm, ValidationError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView

from tasks.models import Task

class UserLoginView(LoginView):
    template_name = "user_login.html"
class UserCreateView(CreateView):
    form_class = UserCreationForm
    template_name = "user_create.html"
    success_url = "/user/login"

def sessions_storage_view(request):

    total_views = request.session.get("total_views",0)
    request.session['total_views'] = total_views + 1
    return HttpResponse(f"Total Views is {total_views}")
class TaskCreateFrom(ModelForm):

    def clean_title(self):
        title = self.cleaned_data["title"]
        if(len(title) < 10):
            raise ValidationError("Data too small")
        return title.upper()

    class Meta:
        model = Task
        fields = ["title", "description", "completed"]

class GenericTaskDeleteView(DeleteView):
    model = Task
    template_name = "task_delete.html"
    success_url = "/tasks"
class GenericDetailTaskView(DetailView):
    model = Task
    template_name = "task_detail.html"
class GenericUpdateTaskView(UpdateView):
    model = Task
    form_class = TaskCreateFrom
    template_name = "task_update.html"
    success_url = "/tasks"
class GenericCreateTaskView(CreateView):
    model = TaskCreateFrom
    fields = ("title", "description", "completed")
    template_name = "task_create.html"
    success_url = "/tasks"
class GenericTaskView(ListView):
    model = Task.objects.filter(deleted=False)
    template_name = "tasks.html"
    context_object_name = "tasks"
    paginate_by = 5

    def get_queryset(self):
        search_term = self.request.GET.get("search")
        tasks = Task.objects.filter(deleted=False)

        if search_term:
            tasks = tasks.filter(title__icontains=search_term)
        return tasks
class CreateTaskView(View):

    def get(self, request):
        return render(request, "task_create.html")

    def post(self, request):
        task_value = request.POST.get("task")
        Task(title=task_value).save()
        return HttpResponseRedirect("/tasks")
class TaskView(View):

    def get(self, request):
        tasks = Task.objects.filter(deleted=False)
        search_term = request.GET.get("search")

        if search_term:
            tasks = tasks.filter(title__icontains=search_term)
        return render(request, "tasks.html", {"tasks": tasks})

    def post(self, request):
        pass

def task_view(request):
    tasks = Task.objects.filter(deleted=False)
    search_term = request.GET.get("search")

    if search_term:
        tasks = tasks.filter(title__icontains=search_term)
    return render(request, "tasks.html", {"tasks": tasks})  

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

