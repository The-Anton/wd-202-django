from django.contrib import admin
from django.urls import path
from tasks.views import (GenericCreateTaskView, GenericTaskDeleteView,
                         GenericTaskView, GenericUpdateTaskView,
                         UserCreateView, UserLoginView, all_task_view, completed_task_view,
                         delete_task_view, done_task_view,
                         sessions_storage_view)
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("tasks/", GenericTaskView.as_view()),
    path("create-task", GenericCreateTaskView.as_view()),
    path("update-task/<pk>", GenericUpdateTaskView.as_view()),
    path("delete-task/<pk>", GenericTaskDeleteView.as_view()),
    path("user/signup", UserCreateView.as_view()),
    path("user/login", UserLoginView.as_view()),
    path("user/logout", LogoutView.as_view()),
    path("completed_task/", completed_task_view),
    path("completed_task/<int:index>/", done_task_view),
    path("all_tasks/", all_task_view),
    path("sessiontest/", sessions_storage_view)


]
