from .models import Alert
from rest_framework import serializers


class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = ["title", "content", "alert_type", "start_at", "end_at"]
