from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from toastapi.models import Advisor
from toastapi.serializers import AdvisorSerializer


class AdvisorList(generics.ListCreateAPIView):
    queryset = Advisor.objects.all()
    serializer_class = AdvisorSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'


class AdvisorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Advisor.objects.all()
    serializer_class = AdvisorSerializer
