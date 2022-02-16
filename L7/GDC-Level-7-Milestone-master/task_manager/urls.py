from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path
from tasks.views import (GenericTaskCreateView, GenericTaskDeleteView,
                         GenericTaskDetailView, GenericTaskUpdateView,
                         GenericTaskView, UserCreateView, UserLoginView,
                         all_task_view, completed_task_view, done_task_view,
                         sessions_storage_view)

from tasks.apiviews import TaskListAPI
from rest_framework.routers import SimpleRouter
from tasks.apiviews import TaskViewSet

router = SimpleRouter()

router.register("api/task", TaskViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("tasks/", GenericTaskView.as_view()),
    path("taskapi/", TaskListAPI.as_view()),
    path("create-task/", GenericTaskCreateView.as_view()),
    path("update-task/<pk>", GenericTaskUpdateView.as_view()),
    path("detail-task/<pk>", GenericTaskDetailView.as_view()),
    path("delete-task/<pk>", GenericTaskDeleteView.as_view()),
    path("user/signup", UserCreateView.as_view()),
    path("user/login", UserLoginView.as_view()),
    path("user/logout", LogoutView.as_view()),
    path("completed_task/", completed_task_view),
    path("completed_task/<int:index>/", done_task_view),
    path("all_tasks/", all_task_view),
    path("sessiontest/", sessions_storage_view),

] + router.urls
