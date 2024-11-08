# Create your views here.

from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
)

from main.models import Student
from main.serializers import StudentSerializer

class StudentListAPIView(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get(self, request):
        return self.list(request)
    def post(self, request):
        return self.create(request)



class StudentAPIView(
    RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView
):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get(self, request, **kwargs):
        return self.retrieve(request, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, **kwargs)

    def delete(self, request, **kwargs):
        return self.destroy(request, **kwargs)