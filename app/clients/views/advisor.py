from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from clients.models import Advisor
from clients.serializers import AdvisorSerializer


class AdvisorList(generics.ListCreateAPIView):
    queryset = Advisor.objects.all()
    serializer_class = AdvisorSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'


class AdvisorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Advisor.objects.all()
    serializer_class = AdvisorSerializer
