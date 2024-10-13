from rest_framework import serializers

from main.models import Study


class StudySerializer(serializers.ModelSerializer):
    class Meta:
        model = Study
        fields = ["id", "name", "description"]
