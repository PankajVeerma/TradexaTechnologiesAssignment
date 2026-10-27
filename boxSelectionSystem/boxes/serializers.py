from rest_framework import serializers

from .models import Box


class BoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Box
        fields = [
            "id",
            "name",
            "length",
            "width",
            "height",
            "max_weight",
            "cost",
        ]
