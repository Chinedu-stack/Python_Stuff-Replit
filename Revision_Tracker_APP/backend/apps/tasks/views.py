from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from apps.tasks.models import Task
from apps.tasks.serializers import TaskSerializer, TaskUpdateSerializer
from apps.tasks.permissions import IsTaskOwner


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsTaskOwner]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['is_completed', 'priority']
    ordering_fields = ['created_at', 'due_date', 'priority']
    ordering = ['-created_at']
    search_fields = ['title', 'description']

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return TaskUpdateSerializer
        return TaskSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def today(self, request):
        today = timezone.now().date()
        tasks = self.get_queryset().filter(start_date__lte=today, end_date__gte=today)
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def overdue(self, request):
        today = timezone.now().date()
        tasks = self.get_queryset().filter(
            due_date__lt=today,
            is_completed=False
        )
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        tasks = self.get_queryset()
        today = timezone.now().date()
        return Response({
            'total': tasks.count(),
            'completed': tasks.filter(is_completed=True).count(),
            'pending': tasks.filter(is_completed=False).count(),
            'today': tasks.filter(start_date__lte=today, end_date__gte=today).count(),
            'overdue': tasks.filter(due_date__lt=today, is_completed=False).count(),
        })

