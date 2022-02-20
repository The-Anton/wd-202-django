from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path
from rest_framework.routers import SimpleRouter
from tasks.apiviews import TaskHistoryViewSet, TaskListAPI, TaskViewSet
from tasks.views import (GenericAllTaskView, GenericTaskCompleteView,
                         GenericTaskCreateView, GenericTaskDeleteView,
                         GenericTaskDetailView, GenericTaskMarkCompletedView,
                         GenericTaskUpdateView, GenericTaskView,
                         UserCreateView, UserLoginView, sessions_storage_view)

router = SimpleRouter()

router.register("api/task", TaskViewSet)
router.register("api/history", TaskHistoryViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("create-task/", GenericTaskCreateView.as_view()),
    path("update-task/<pk>", GenericTaskUpdateView.as_view()),
    path("detail-task/<pk>", GenericTaskDetailView.as_view()),
    path("delete-task/<pk>", GenericTaskDeleteView.as_view()),
    path("completed_task/<pk>", GenericTaskMarkCompletedView.as_view()),
    path("user/signup", UserCreateView.as_view()),
    path("user/login", UserLoginView.as_view()),
    path("user/logout", LogoutView.as_view()),
    path("tasks/", GenericTaskView.as_view()),
    path("completed_task/", GenericTaskCompleteView.as_view()),
    path("all_tasks/", GenericAllTaskView.as_view()),
    path("sessiontest/", sessions_storage_view),

]+ router.urls
