from asyncio import tasks
from dataclasses import field
from random import choices

from django.contrib.auth.models import User
from django.http.response import JsonResponse
from django.views import View
from django_filters.rest_framework import (BooleanFilter, CharFilter, ChoiceFilter, DateTimeFilter,
                                           DjangoFilterBackend, FilterSet)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from tasks.models import History, Task, STATUS_CHOICES


class TaskFilter(FilterSet):
    title = CharFilter(lookup_expr="icontains")
    completed = BooleanFilter(field_name="completed")
    status = ChoiceFilter(field_name="status")

class HistoryFilter(FilterSet):
    change_time = DateTimeFilter(field_name="change_time")
    old_status = ChoiceFilter(choices=STATUS_CHOICES)
    new_status = ChoiceFilter(choices=STATUS_CHOICES)


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "username")
    
class TaskSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Task
        fields = ["id", "title", "description", "completed", "status", "user"]

class HistorySerializer(ModelSerializer):
    task = TaskSerializer(read_only=True)
    class Meta:
        model = History
        fields = ["task", "old_status", "new_status", "change_time"]

class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer 

    permission_classes = (IsAuthenticated,)

    filter_backends = (DjangoFilterBackend,)
    filterset_class = TaskFilter

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user, deleted=False)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        new_status = serializer.validated_data["status"]
        task = Task.objects.get(id=self.kwargs["pk"])
        serializer.save()

        if new_status != task.status:
            task_history = History(old_status = task.status, new_status = new_status, task = task)
            task_history.save()

        

class TaskHistoryViewSet(ReadOnlyModelViewSet):
    queryset = History.objects.all()
    serializer_class = HistorySerializer

    permission_classes = (IsAuthenticated,)

    filter_backends = (DjangoFilterBackend,)
    filterset_class = HistoryFilter

    def get_queryset(self):
        return History.objects.all()

class TaskListAPI(APIView):

    def get(self, request):
        tasks = Task.objects.filter(deleted=False)
        data = []

        for task in tasks:
            data.append({"title" : task.title})
        return Response({"tasks" : data})
