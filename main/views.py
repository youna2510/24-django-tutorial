# Create your views here.
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Study
from django.contrib.auth import login, authenticate
from main.serializers import StudySerializer, LoginSerializer, UserSerializer
from rest_framework import generics


class LoginView(GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            request,
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
        )

        if not user:
            raise AuthenticationFailed("아이디 또는 비밀번호가 틀렸습니다")

        login(request, user)

        return Response()


class SignupView(generics.CreateAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = UserSerializer


class StudyListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Study.objects.all()
    serializer_class = StudySerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class StudyDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Study.objects.all()
    serializer_class = StudySerializer

    def get_queryset(self):
        if self.request.method == "GET":
            return super().get_queryset()

        return super().get_queryset().filter(created_by=self.request.user)
