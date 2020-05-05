from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination


class ClientDependenceList(generics.ListCreateAPIView):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return self.serializer_class.CreateSerializer
        return self.serializer_class


class ClientDependenceDetail(generics.RetrieveUpdateDestroyAPIView):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'
