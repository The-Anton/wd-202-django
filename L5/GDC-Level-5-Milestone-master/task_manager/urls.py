from django.contrib import admin

from django.urls import path

from tasks.views import delete_task_view, task_view, add_task_view, delete_task_view, completed_task_view, done_task_view, all_task_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("tasks/", task_view),
    path("add-task/", add_task_view),
    path("delete-task/<int:index>", delete_task_view),
    path("completed_task/", completed_task_view),
    path("completed_task/<int:index>/", done_task_view),
    path("all_tasks/", all_task_view)
]
