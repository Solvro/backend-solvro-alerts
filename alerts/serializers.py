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
            "open_in_new_tab",
            "is_global",
            "is_dismissable",
            "start_at",
            "end_at",
        ]
