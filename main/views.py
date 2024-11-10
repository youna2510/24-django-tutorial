# Create your views here.
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (
    ListModelMixin,
    DestroyModelMixin,
    CreateModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Study, StudyParticipation
from django.contrib.auth import login, authenticate
from main.serializers import (
    StudySerializer,
    LoginSerializer,
    UserSerializer, StudyParticipationSerializer
)
from rest_framework import generics, status


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


class StudyParticipationListView(
    ListModelMixin,
    CreateModelMixin,
    GenericAPIView,
):
    """
    GET: 내 스터디 참여 목록. 남의 것이 조회되면 안됩니다.
    POST: 내 스터디 참여 목록 추가. 남의 것을 추가할 수 없습니다(HTTP 403 에러)
    """

    ### assignment3: 이곳에 과제를 작성해주세요
    permission_classes = [IsAuthenticated]
    queryset = StudyParticipation.objects.all()
    serializer_class = StudyParticipationSerializer

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = StudyParticipationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if request.user !=serializer.validated_data["user"] :
            return Response("남의 것을 추가할 수 없습니다.", status=status.HTTP_403_FORBIDDEN)
        return self.create(request, *args, **kwargs)

    ### end assignment3


class StudyParticipationView(
    DestroyModelMixin,
    GenericAPIView,
):
    """
    DELETE: 내 스터디 참여 목록 제거. 남의 것을 제거할 수 없습니다(HTTP 404 에러)
    """

    ### assignment3: 이곳에 과제를 작성해주세요
    permission_classes = [IsAuthenticated]
    queryset = StudyParticipation.objects.all()
    serializer_class = StudyParticipationSerializer

    def delete(self, request, *args, **kwargs):
        instance=self.get_object()
        if request.user!= instance.user:
            return Response("남의 것을 제거할 수 없습니다", status=status.HTTP_404_NOT_FOUND)
        return self.destroy(request, *args, **kwargs)

    ### end assignment3
