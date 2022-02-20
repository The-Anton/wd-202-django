from re import template
from urllib import request

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.forms import ModelForm, ValidationError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from tasks.models import Task


class AuthorisedTaskManager(LoginRequiredMixin):
    def get_queryset(self):
        return Task.objects.filter(deleted=False, user=self.request.user)
class UserLoginView(LoginView):
    template_name = "user_login.html"
class UserCreateView(CreateView):
    form_class = UserCreationForm
    template_name = "user_create.html"
    success_url = "/user/login"

def sessions_storage_view(request):

    total_views = request.session.get("total_views",0)
    request.session['total_views'] = total_views + 1
    return HttpResponse(f"Total Views is {total_views} an the user is {request.user}")

class TaskCreateFrom(ModelForm):

    def clean_title(self):
        title = self.cleaned_data["title"]
        if(len(title) < 10):
            raise ValidationError("Data too small")
        return title.upper()

    class Meta:
        model = Task
        fields = ["title", "description", "completed"]

class GenericTaskDeleteView(AuthorisedTaskManager, DeleteView):
    model = Task
    template_name = "task_delete.html"
    success_url = "/tasks"

class GenericTaskDetailView(AuthorisedTaskManager, DetailView):
    model = Task
    template_name = "task_detail.html"
class GenericTaskUpdateView(AuthorisedTaskManager, UpdateView):
    model = Task
    form_class = TaskCreateFrom
    template_name = "task_update.html"
    success_url = "/tasks"

class GenericTaskCreateView(CreateView):
    form_class = TaskCreateFrom
    template_name = "task_create.html"
    success_url = "/tasks"

    def form_valid(self, form):
        task = Task.objects.all().filter(completed=False, priority=form.priority)
        if task:
            update_priority()
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

class GenericTaskCompleteView(LoginRequiredMixin, ListView):
    queryset = Task.objects.all().filter(completed=True)
    template_name = "completed.html"
    context_objext_name = "completed_tasks"
    paginate_by = 5

class GenericTaskMarkCompletedView(LoginRequiredMixin, View):

    def get_queryset(self, index):
        Task.objects.filter(id=index).update(completed=True)
        return HttpResponseRedirect("/tasks")

class GenericTaskView(LoginRequiredMixin, ListView):
    queryset = Task.objects.filter(deleted=False)
    template_name = "tasks.html"
    context_object_name = "tasks"
    paginate_by = 5

    def get_queryset(self):
        search_term = self.request.GET.get("search")
        tasks = Task.objects.filter(deleted=False, user=self.request.user)

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

