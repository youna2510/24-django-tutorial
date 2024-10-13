from rest_framework import serializers

from main.models import Study


class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Study
        fields = ["id", "name", "description"]
