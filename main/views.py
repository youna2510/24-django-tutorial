# Create your views here.

from main.models import Study
from main.serializers import StudySerializer
from rest_framework import generics


class StudyListView(generics.ListCreateAPIView):
    queryset = Study.objects.all()
    serializer_class = StudySerializer


class StudyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Study.objects.all()
    serializer_class = StudySerializer
