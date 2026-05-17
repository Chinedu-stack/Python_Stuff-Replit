from rest_framework import serializers
from apps.tasks.models import Task
from apps.accounts.serializers import UserSerializer


class TaskSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = (
            'id', 'user', 'title', 'description', 'is_completed',
            'start_date', 'end_date', 'due_date', 'priority',
            'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')

    def validate(self, data):
        if data.get('start_date') and data.get('end_date'):
            if data['start_date'] > data['end_date']:
                raise serializers.ValidationError('Start date must be before end date.')
        return data


class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            'title', 'description', 'is_completed',
            'start_date', 'end_date', 'due_date', 'priority'
        )

    def validate(self, data):
        if data.get('start_date') and data.get('end_date'):
            if data['start_date'] > data['end_date']:
                raise serializers.ValidationError('Start date must be before end date.')
        return data
