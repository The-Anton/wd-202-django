from asyncio import tasks
from django.views import View
from django.http.response import JsonResponse

from tasks.models import Task
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet

class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = ["title", "description", "completed"]

class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class TaskListAPI(View):

    def get(self, request):
        tasks = Task.objects.filter(deleted=False)
        data = []

        for task in tasks:
            data.append({"title" : task.title})
        return JsonResponse({"tasks" : data})