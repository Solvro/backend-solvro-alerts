from rest_framework import serializers

from .models import Alert


class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = [
            "id",
            "title",
            "content",
            "alert_type",
            "link",
            "is_global",
            "is_dismissable",
            "start_at",
            "end_at",
        ]
