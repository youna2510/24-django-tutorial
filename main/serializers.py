from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from main.models import Study, User


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "password"]

    def save(self, **kwargs):
        hashed_password = make_password(self.validated_data["password"])
        return super().save(password=hashed_password, **kwargs)


class StudySerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )

    class Meta:
        model = Study
        fields = ["id", "name", "description", "created_by"]
