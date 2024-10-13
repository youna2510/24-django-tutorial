from rest_framework import serializers

from main.models import Study


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class StudySerializer(serializers.ModelSerializer):
    class Meta:
        model = Study
        fields = ["id", "name", "description"]
