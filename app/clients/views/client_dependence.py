from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics


class ClientDependenceList(generics.ListCreateAPIView):
    lookup_field = 'client'
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'

    def perform_create(self, serializer):
        serializer.save(client_id=self.kwargs.get('client'))


class ClientDependenceDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_fields = ['client', 'pk']
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'
