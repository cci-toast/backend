from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from clients.models import Client
from clients.serializers import ClientSerializer

from rest_framework.permissions import IsAuthenticated


class ClientList(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'


class ClientDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
